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