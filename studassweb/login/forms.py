from django import forms
from django.utils.translation import ugettext as _

class LoginForm(forms.Form):
    user_name = forms.CharField(label=_('User name: '))
    password = forms.CharField(label=_('Password: '), widget=forms.PasswordInput())