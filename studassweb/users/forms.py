from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from base.models import SiteConfiguration
import datetime


class LoginForm(forms.Form):
    user_name = forms.CharField(label=_('User name'))
    password = forms.CharField(label=_('Password'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # add the css class for bootstrap
        self.fields['user_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def clean(self):
        super(LoginForm, self).clean()
        # https://docs.djangoproject.com/en/1.7/topics/auth/default/#auth-web-requests

        # if username or password is missing, there's already an error, so just skip trying to authenticate.
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
    user_name = forms.CharField(label=_("User name"), min_length=6, max_length=20)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password_repeat = forms.CharField(label=_("Repeat password"), widget=forms.PasswordInput)
    first_name = forms.CharField(label=_("First name"), max_length=50)
    last_name = forms.CharField(label=_("Last name"), max_length=50)
    email = forms.EmailField(label=_("Email"), )
    member = forms.BooleanField(label=_("Are you a member of this organization?"), initial=False)
    enrollment_year = forms.IntegerField(label=_("Enrollment year"), required=False, initial=datetime.datetime.now().year)
    graduation_year = forms.IntegerField(label=_("Graduation year (leave empty if still studying)"), required=False)

    def clean(self):
        super(RegisterForm, self).clean()
        if not self.errors:
            # check that the user doesn't exist already
            if User.objects.filter(username=self.cleaned_data['user_name']).count() != 0:
                self._errors['user_name'] = _("The username is taken")

            # check that the email isn't already registered to an account
            if User.objects.filter(email=self.cleaned_data['email']).count() != 0:
                self._errors['graduation_year'] = _("An account associated to this email already exists")

            # if the user claims hes a member, make sure that the enrollment and graduation years make sense
            if self.cleaned_data['member']:
                enroll = self.cleaned_data['enrollment_year']
                graduate = self.cleaned_data['graduation_year']
                if enroll < SiteConfiguration.founded():
                    self._errors['enrollment_year'] = _("You can't have enrolled before the association was created.")
                if graduate:
                    if graduate <= enroll:
                        self._errors['graduation_year'] = _("You can't have graduated before you enrolled")
