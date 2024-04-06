from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TelegramAccount
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle


@login_required(login_url='login')
def telegram_account_list(request):
    if request.method == 'POST' and 'delete_account_id' in request.POST:
        account_id = request.POST.get('delete_account_id')
        account = get_object_or_404(TelegramAccount, pk=account_id)
        account.delete()
        return redirect('telegram_account_list')
    
    accounts = TelegramAccount.objects.all()
    return render(request, 'app/telegram_account_list.html', {'accounts': accounts})


@login_required(login_url='login')
def create_telegram_account(request):
    if request.method == 'POST':
        api_id = request.POST['api_id']
        api_hash = request.POST['api_hash']
        phone_number = request.POST['phone_number']
        # Get the currently logged-in user
        user = request.user
        TelegramAccount.objects.create(user=user, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        return redirect('telegram_account_list')
    return render(request, 'app/create_telegram_account.html')



@login_required(login_url='login')
def delete_account(request, account_id):
    account = TelegramAccount.objects.get(id=account_id)
    account.delete()
    return redirect('telegram_account_list')


def filter_banned_accounts(request):
    # Fetch all accounts from database
    accounts = TelegramAccount.objects.all()
    banned_accounts = []

    # Filter out banned accounts
    for account in accounts:
        client = TelegramClient(f'sessions/{account.phone_number}', account.api_id, account.api_hash)
        client.connect()
        if not client.is_user_authorized():
            banned_accounts.append(account)

    return render(request, 'filter_banned_accounts.html', {'banned_accounts': banned_accounts})

# =====================================Scraper OF Telegram Member=================================

from django.http import HttpResponse
from concurrent.futures import ThreadPoolExecutor
import asyncio
from io import StringIO
import csv
import datetime
from .models import TelegramAccount, TelegramUser
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.types import UserStatusOffline
from telethon.sessions import MemorySession
from django.shortcuts import render, redirect

# Define a thread pool executor
executor = ThreadPoolExecutor()

# Define an asynchronous function to scrape telegram users
async def scrape_telegram_users_async(telegram_account, group_name, code):
    try:
        # Create a Telethon session with MemorySession
        client = TelegramClient(MemorySession(), telegram_account.api_id, telegram_account.api_hash)
        await client.connect()

        # Check if the user is already authorized
        if not await client.is_user_authorized():
            # Redirect to a page to enter the login code
            return redirect('enter_login_code')

        # Get group information
        group = await client.get_entity(group_name)

        # Scrape users based on choice
        members = await client.iter_participants(group, aggressive=True)

        # Save scraped users to database
        for member in members:
            TelegramUser.objects.create(
                username=member.username,
                user_id=member.id,
                access_hash=member.access_hash,
                group=group.title,
                group_id=group.id,
                status=type(member.status).__name__,
                was_online=member.status.was_online if isinstance(member.status, UserStatusOffline) else None
            )

        # Save scraped users to CSV file
        csv_filename = f'telegram_members_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        csv_content = StringIO()
        fieldnames = ['username', 'user_id', 'group', 'group_id', 'status', 'was_online']
        writer = csv.DictWriter(csv_content, fieldnames=fieldnames)
        writer.writeheader()
        for member in members:
            writer.writerow({
                'username': member.username,
                'user_id': member.id,
                'group': group.title,
                'group_id': group.id,
                'status': type(member.status).__name__,
                'was_online': member.status.was_online if isinstance(member.status, UserStatusOffline) else None
            })

        # Provide download link for CSV file
        return csv_content.getvalue(), csv_filename

    except PhoneNumberBannedError:
        # Handle banned phone number
        raise RuntimeError('Phone number is banned')
    except Exception as e:
        raise RuntimeError(str(e))

# Define a view function for entering the login code
def enter_login_code(request):
    if request.method == 'POST':
        # Get the login code from form data
        code = request.POST.get('login_code')
        if code:
            # If code is provided, proceed to scrape telegram users
            group_name = request.session.get('group_name')
            return redirect('scrape_telegram_users', group_name=group_name, code=code)
    # Render the form to enter the login code
    return render(request, 'app/telegram_login.html')

# Define a view function for scraping telegram users
def scrape_telegram_users(request, group_name=None, code=None):
    if request.method == 'POST':
        try:
            # Access the TelegramAccount associated with the current user
            telegram_account = request.user.telegramaccount
        except TelegramAccount.DoesNotExist:
            return render(request, 'app/error.html', {'message': 'Telegram account not found'})

        # Get group name from form data
        group_name = request.POST.get('group_name')

        # Store group name in session
        request.session['group_name'] = group_name

        if not group_name:
            return render(request, 'app/error.html', {'message': 'Group name is required'})

        # If code is provided, proceed with scraping
        if code:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Run the asynchronous function in a separate thread
            future = loop.run_in_executor(executor, scrape_telegram_users_async, telegram_account, group_name, code)

            # Get the result from the future
            try:
                csv_content, csv_filename = loop.run_until_complete(future)
            finally:
                loop.close()

            # Provide download link for CSV file
            response = HttpResponse(csv_content, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{csv_filename}"'
            return response
        else:
            # Redirect to enter login code
            return redirect('enter_login_code')
    else:
        # Render the form to enter the group name
        return render(request, 'app/fetch_telegram_members.html')



#====================================================Add Telegram Member==========================
from django.shortcuts import render
from django.views import View
from django.conf import settings
from .models import TelegramAccount
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from asgiref.sync import async_to_sync
import csv
import time
import random
import pyfiglet
from colorama import init, Fore
import os

init()

class TelegramAdderView(View):
    def get(self, request):
        return render(request, 'app/telegram_adder.html')

    def post(self, request):
        r = Fore.RED
        g = Fore.GREEN
        rs = Fore.RESET
        w = Fore.WHITE
        cy = Fore.CYAN
        ye = Fore.YELLOW
        colors = [r, g, w, ye, cy]
        info = g + '[' + w + 'i' + g + ']' + rs
        attempt = g + '[' + w + '+' + g + ']' + rs
        sleep = g + '[' + w + '*' + g + ']' + rs
        error = g + '[' + r + '!' + g + ']' + rs

        authenticated_user = request.user

        try:
            telegram_account = TelegramAccount.objects.get(user=authenticated_user)
        except TelegramAccount.DoesNotExist:
            return render(request, 'app/telegram_adder.html', {'error_message': "Telegram account not found."})

        api_id = telegram_account.api_id
        api_hash = telegram_account.api_hash
        phone = telegram_account.phone_number

        file = request.FILES.get('file')
        group = request.POST.get('group')

        def banner():
            f = pyfiglet.Figlet(font='slant')
            logo = f.renderText('Telegram')
            print(random.choice(colors) + logo + rs)
            print(f'{info}{g} Telegram Adder[USERNAME] V1.1{rs}')
            print(f'{info}{g} Author: github.com/denizshabani{rs}\n')

        def clscreen():
            os.system('cls')

        clscreen()
        banner()

        class Relog:
            def __init__(self, lst, filename):
                self.lst = lst
                self.filename = filename
            
            def start(self):
                with open(self.filename, 'w', encoding='UTF-8') as f:
                    writer = csv.writer(f, delimiter=",", lineterminator="\n")
                    writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
                    for user in self.lst:
                        writer.writerow([user['username'], user['id'], user['access_hash'], user['group'], user['group_id']])
                    f.close()

        def update_list(lst, temp_lst):
            count = 0
            while count != len(temp_lst):
                del lst[0]
                count += 1
            return lst

        users = []
        # Handle the uploaded file directly from memory
        file_data = file.read().decode('utf-8').splitlines()
        for row in csv.reader(file_data, delimiter=','):
            user = {}
            user['username'] = row[0]
            user['user_id'] = row[1]
            user['access_hash'] = row[2]
            user['group'] = row[3]
            user['group_id'] = row[4]
            users.append(user)

        # Use MySQL as the session storage backend for Telethon
        session_directory = os.path.join(settings.BASE_DIR, 'sessions')
        session_name = f'{session_directory}/{phone}'

        # Ensure the sessions directory exists
        if not os.path.exists(session_directory):
            os.makedirs(session_directory)

        session = f'mysql://{settings.DATABASES["default"]["USER"]}:{settings.DATABASES["default"]["PASSWORD"]}@{settings.DATABASES["default"]["HOST"]}/{settings.DATABASES["default"]["NAME"]}'

        async def add_members():
            client = TelegramClient(session_name, api_id, api_hash)
            client.connect()
            time.sleep(1.5)
            target_group = await client.get_entity(group)
            entity = InputPeerChannel(target_group.id, target_group.access_hash)
            group_name = target_group.title
            print(f'{info}{g} Adding members to {group_name}{rs}\n')
            n = 0
            added_users = []
            for user in users:
                n += 1
                added_users.append(user)
                if n % 50 == 0:
                    print(f'{sleep}{g} Sleep 2 min to prevent possible account ban{rs}')
                    time.sleep(120)
                try:
                    if user['username'] == "":
                        continue
                    user_to_add = await client.get_input_entity(user['username'])
                    await client(InviteToChannelRequest(entity, [user_to_add]))
                    usr_id = user['user_id']
                    print(f'{attempt}{g} Adding {usr_id}{rs}')
                    print(f'{sleep}{g} Sleep 30s{rs}')
                    time.sleep(30)
                except PeerFloodError:
                    os.system(f'del {file}')
                    return {'error_message': "Aborted. Peer Flood Error"}
                except UserPrivacyRestrictedError:
                    print(f'{error}{r} User Privacy Restriction{rs}')
                    continue
                except KeyboardInterrupt:
                    print(f'{error}{r} Aborted. Keyboard Interrupt{rs}')
                    update_list(users, added_users)
                    if not len(users) == 0:
                        print(f'{info}{g} Remaining users logged to {file}')
                        logger = Relog(users, file)
                        logger.start()
                except Exception as e:
                    print(f'{error}{r} Some Other error in adding{rs}')
                    print(e)
                    continue
            return {'success_message': "Adding complete. Press enter to exit."}

        return async_to_sync(add_members)()
