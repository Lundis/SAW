from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login

class LoginForm(forms.Form):
    user_name = forms.CharField(label=_('User name'))
    password = forms.CharField(label=_('Password'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # add the css class for bootstrap
        self.fields['user_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        # https://docs.djangoproject.com/en/1.7/topics/auth/default/#auth-web-requests

        # if username or password is missing, there's already an error, so just skip trying to log in.
        if 'user_name' in self.cleaned_data and 'password' in self.cleaned_data:
            username = self.cleaned_data['user_name']
            pw = self.cleaned_data['password']
            if username and pw:
                user = authenticate(username=username, password=pw)
            if not user:
                self.add_error(None, _("Wrong username/password"))
            elif not user.is_active:
                self.add_error(None, _("Your account is disabled"))


    def login_user(self, request):
        user = authenticate(username=self.cleaned_data['user_name'], password=self.cleaned_data['password'])
        login(request, user)

class RegisterForm(forms.Form):
    pass