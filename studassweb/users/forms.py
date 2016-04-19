from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from .models import UserExtension, KerberosServer
from base.forms import SortingForm
from base.validators import validate_password, validate_username
from .groups import put_perm_in_standard_group
from captcha.fields import ReCaptchaField
import logging

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    user_name = forms.CharField(label=_('User name'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())

    def clean(self):
        super().clean()
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
        # UserExtension is normally created when creating user, except for SuperUsers.
        try:
            UserExtension.objects.get(user=user)
        except UserExtension.DoesNotExist:
            UserExtension.create_for_user(user)
            logging.warning('UserExtension for user %s was created at login' % user.username)
        login(request, user)


class RegisterForm(forms.Form):
    user_name = forms.CharField(label=_("User name"), min_length=3, max_length=20)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password_repeat = forms.CharField(label=_("Repeat password"), widget=forms.PasswordInput)
    first_name = forms.CharField(label=_("First name"), max_length=50)
    last_name = forms.CharField(label=_("Last name"), max_length=50)
    email = forms.EmailField(label=_("Email"))

    captcha = ReCaptchaField()

    def clean_user_name(self):
        validate_username(self.cleaned_data['user_name'])
        # check that the user doesn't exist already
        if User.objects.filter(username=self.cleaned_data['user_name']).count() != 0:
            raise ValidationError(_("The username is taken"))
        return self.cleaned_data['user_name']

    def clean_email(self):
        # check that the email isn't already registered to an account
        if User.objects.filter(email=self.cleaned_data['email']).count() != 0:
            raise ValidationError(_("An account associated to this email already exists"))
        return self.cleaned_data['email']

    def clean_password(self):
        validate_password(self.cleaned_data['password'])
        return self.cleaned_data['password']

    def clean(self):
        super().clean()
        if 'password' in self.cleaned_data and self.cleaned_data['password_repeat'] != self.cleaned_data['password']:
            self.add_error('password_repeat', _("The passwords are not equal"))

    def save(self):
        if self.is_valid():
            # create the user
            return UserExtension.create_user(self.cleaned_data['user_name'],
                                             self.cleaned_data['password'],
                                             self.cleaned_data['first_name'],
                                             self.cleaned_data['last_name'],
                                             self.cleaned_data['email'])


class UserBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def save(self, commit=True):
        """
        Mark the user as complete
        :param commit:
        :return:
        """
        user = super().save(commit=commit)
        user_ext = UserExtension.objects.get(user=user)
        user_ext.incomplete = False
        if commit:
            user_ext.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta():
        model = UserExtension
        fields = ('avatar', 'description', 'link_to_homepage')


class CustomGroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = ("name",)


class PermissionEditorForm(SortingForm):

    def save(self):
        for group, sawps_and_ids in self.cleaned_items().values():
            for sawp_and_id in sawps_and_ids:
                sawp = sawp_and_id['item']
                put_perm_in_standard_group(sawp, group)


class KerberosServerForm(forms.ModelForm):
    class Meta:
        model = KerberosServer
        fields = ("hostname", "realm", "service")