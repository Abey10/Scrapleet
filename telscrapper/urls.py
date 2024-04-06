from django.urls import path
from . import views
from .views import TelegramAdderView

urlpatterns = [
    path('accounts/', views.telegram_account_list, name='telegram_account_list'),
    path('accounts/create/', views.create_telegram_account, name='create_telegram_account'),
    path('delete/<int:account_id>/', views.delete_account, name='delete_account'),
    path('scrape/', views.scrape_telegram_users, name='scrape_telegram_users'),
    path('tellogin/', views.enter_login_code, name='enter_login_code'),
    path('telegram-adder/', TelegramAdderView.as_view(), name='telegram_adder'),
]
