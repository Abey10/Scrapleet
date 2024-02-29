from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required

# All Registration 
# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()

#             # Create UserProfile for the user
#             UserProfile.objects.create(user=user)

#             login(request, user)
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'app/signup.html', {'form': form})

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create UserProfile for the user
            UserProfile.objects.create(user=user)

            # Send registration email notification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'

            # Load both HTML and plain text versions of the email content
            html_message = render_to_string('app/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            plain_message = strip_tags(html_message)

            try:
                # Send email with both HTML and plain text versions
                email = EmailMultiAlternatives(subject, plain_message, 'admin@jexceltech.com.ng', [user.email])
                email.attach_alternative(html_message, "text/html")
                email.send()
            except Exception as e:
                # Handle email sending failure
                print("Error sending activation email:", e)

            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/signup.html', {'form': form})


# All Login
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'app/signin.html', {'form': form})


def logout_user(request):
    auth_logout(request)
    return redirect('login')

# Google Login

from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

def google_login(request):
    # Check if there is a user signed in through Firebase
    if request.method == 'POST' and request.user.is_authenticated:
        # Get user data from Firebase
        firebase_user_id = request.POST.get('firebase_user_id')
        email = request.POST.get('email')
        # Assuming you have a custom User model with an 'email' field
        user = authenticate(request, email=email, firebase_user_id=firebase_user_id)
        if user is not None:
            # If the user exists in your Django database, log them in
            login(request, user)
            # Redirect the user to the home page or any desired page
            return redirect('home')
        else:
            # If the user does not exist, return a bad request response
            return HttpResponseBadRequest("User does not exist in the system.")
    else:
        # If the request method is not POST or the user is not authenticated,
        # redirect the user to the login page or any desired page
        return redirect('login')


# Activate

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # You can add any additional logic here, such as redirecting to a success page or displaying a message
        return render(request, 'app/activation_success.html') 
    else:
        # Handle invalid activation link, e.g., display an error message or redirect to an error page
        return render(request, 'app/activation_failure.html')  


# User Profile

@login_required(login_url='login')
def profile(request):
    # Fetch user profile details
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/profile.html', context)