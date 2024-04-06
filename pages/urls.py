from django.urls import path
from .views import ( 
    home, blog, faq, 
    pricing, testimonial, 
    terms, settings, support, 
    activity, billing, blog_details, 
    create_blog, addfund, services,
    orders, new_orders, mass_orders,
    makemoney, howtouse, update
)

urlpatterns = [
    path('', home, name='home'),
    path('blog/', blog, name='blog'),
    path('faq/', faq, name='faq'),
    path('pricing/', pricing, name='pricing'),
    path('testimonial/', testimonial, name='testimonial'),
    path('terms/', terms, name='terms'),
    path('settings/', settings, name='settings'),
    path('support/', support, name='support'),
    path('activity/', activity, name='activity'),
    path('billing/', billing, name='billing'),
    path('blog/<int:blog_id>/', blog_details, name='blog-details'),
    path('blog/create/', create_blog, name='create_blog'),
    path('addfund/', addfund, name='addfund'),
    path('services/', services, name='services'),
    path('orders/', orders, name='orders'),
    path('new_orders/', new_orders, name='new_orders'),
    path('mass_orders/', mass_orders, name='mass_orders'),
    path('makemoney/', makemoney, name='makemoney'),
    path('howtouse/', howtouse, name='howtouse'),
    path('update/', update, name='update'),
]