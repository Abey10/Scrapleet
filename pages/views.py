from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from users.models import UserProfile
from .models import Blog
from .forms import BlogForm


@login_required(login_url='login')
def home(request):
    # Fetch user profile details
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/index-2.html', context)


@login_required(login_url='login')
def blog(request):
    user_profile = UserProfile.objects.get(user=request.user)
    blogs = Blog.objects.all()
    context = {'user_profile': user_profile, 'blogs': blogs}
    return render(request, 'app/blog.html', context)

@login_required(login_url='login')
def blog_details(request, blog_id):
    user_profile = UserProfile.objects.get(user=request.user)
    blog = get_object_or_404(Blog, pk=blog_id)
    blogs = Blog.objects.order_by('-created_at')[:5]
    context = {'user_profile': user_profile, 'blog': blog, 'blogs': blogs}
    return render(request, 'app/blog-details.html', context)


@login_required(login_url='login')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog')
    else:
        form = BlogForm()

    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile, 'form': form}
    return render(request, 'app/create-blog.html', context)


@login_required(login_url='login')
def faq(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/faq.html', context)


@login_required(login_url='login')
def pricing(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/pricing.html', context)


@login_required(login_url='login')
def testimonial(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/testimonial.html', context)

@login_required(login_url='login')
def terms(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/terms.html', context)


@login_required(login_url='login')
def settings(request):
    # Get the user's profile instance or create a new one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = UserProfileForm(instance=profile)
    
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile, 'form': form}

    return render(request, 'app/settings.html', context)


@login_required(login_url='login')
def billing(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/billing.html', context)


@login_required(login_url='login')
def activity(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/activity.html', context)


@login_required(login_url='login')
def support(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/help.html', context)


@login_required(login_url='login')
def addfund(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/addfund.html', context)


@login_required(login_url='login')
def orders(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/orders.html', context)


@login_required(login_url='login')
def new_orders(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/new_orders.html', context)


import requests
from django.shortcuts import render
from .models import Service  

@login_required(login_url='login')
def services(request):
    # Fetch data from SMMStone API
    api_url = 'https://smmstone.com/api/v2'
    api_key = '8103854ffdc487739b71d64fcc4c1806'
    payload = {'key': api_key, 'action': 'services'}
    response = requests.get(api_url, params=payload)
    data = response.json()

    # Store fetched data in models
    for item in data:
        service = Service.objects.create(
            service_id=item['service'],
            name=item['name'],
            type=item['type'],
            rate=item['rate'],
            min=item['min'],
            max=item['max'],
            dripfeed=item['dripfeed'],
            refill=item['refill'],
            cancel=item['cancel'],
            category=item['category']
        )

    # Fetch all services from your database
    services = Service.objects.all()

    # Pass services data to the template for rendering
    context = {'services': services}
    return render(request, 'app/services.html', context)



@login_required(login_url='login')
def mass_orders(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/mass_orders.html', context)


@login_required(login_url='login')
def makemoney(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/makemoney.html', context)


@login_required(login_url='login')
def howtouse(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/howtouse.html', context)


@login_required(login_url='login')
def update(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'app/update.html', context)