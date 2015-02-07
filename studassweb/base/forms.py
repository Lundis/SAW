from django import forms
from django.forms import ValidationError
from .models import SiteConfiguration, BootswatchTheme, Feedback


class ConfirmationForm(forms.Form):
    confirmation_box = forms.BooleanField(widget=forms.CheckboxInput, required=True)


class BootswatchThemeSelectForm(forms.Form):
    theme = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(BootswatchThemeSelectForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(BootswatchThemeSelectForm, self).clean()
        if not 'theme' in self.cleaned_data:
            raise ValidationError("No theme was specified")
        theme_name = self.cleaned_data['theme']
        try:
            theme = BootswatchTheme.objects.get(name=theme_name)
        except BootswatchTheme.DoesNotExist:
            raise ValidationError("Theme " + theme_name + " does not exist")

    def save(self):
        settings = SiteConfiguration.instance()
        theme = BootswatchTheme.objects.get(name=self.cleaned_data['theme'])
        settings.bootstrap_theme_url = theme.theme_path
        settings.bootstrap_theme_mod_url = None
        settings.save()


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ("response", "url",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.type = kwargs.pop('type')
        super(FeedbackForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        super(FeedbackForm, self).is_valid()
        if Feedback.can_user_give_feedback(user=self.request.user,
                                           ip=self.request.META.get('REMOTE_ADDR'),
                                           type=self.type,
                                           url=self.cleaned_data['url']):

            return True
        else:
            raise ValidationError("You cannot give feedback on this element")

    def save(self, commit=True):
        feedback = super(FeedbackForm, self).save(commit=False)
        feedback.type = self.type
        if self.request.user.is_authenticated:
            feedback.user = self.request.user
        feedback.ip_address = self.request.META['REMOTE_ADDR']
        if commit:
            feedback.save()
        return feedback