from django import forms
from .models import TelegramAccount

# class TelegramAccountForm(forms.ModelForm):
#     class Meta:
#         model = TelegramAccount
#         fields = ['username', 'api_id', 'api_hash','is_admin', 'has_permission_to_add_members']


# class FetchMembersForm(forms.Form):
#     channel_link = forms.CharField(label='Channel Link')
#     telegram_account = forms.ModelChoiceField(queryset=TelegramAccount.objects.all(), label='Telegram Account')


# class FetchMembersForm(forms.Form):
#     channel_link = forms.CharField(label='Channel Link')
#     telegram_account = forms.ModelChoiceField(queryset=TelegramAccount.objects.none(), label='Telegram Account')

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  # Get the current user
#         super(FetchMembersForm, self).__init__(*args, **kwargs)
#         if user:
#             telegram_accounts = TelegramAccount.objects.filter(user=user)
#             self.fields['telegram_account'].queryset = telegram_accounts
