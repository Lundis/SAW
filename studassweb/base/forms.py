from django import forms
from django.forms import ValidationError
from .models import SiteConfiguration, BootswatchTheme


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