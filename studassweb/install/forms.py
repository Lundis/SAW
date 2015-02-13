from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from base.models import SiteConfiguration, DisabledModule
import datetime


# TODO for all forms: sanitize input according to the requirements / design.


class AssociationForm(forms.Form):
    name = forms.CharField(label=_('Association name'))
    contact_email = forms.EmailField(label=_('Association contact email'))
    founded = forms.IntegerField(label=_('Founded year'), min_value=0, max_value=datetime.datetime.now().year)

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = SiteConfiguration.instance().association_name
        self.fields['contact_email'].initial = SiteConfiguration.instance().association_contact_email
        self.fields['founded'].initial = SiteConfiguration.founded()

    def clean(self):
        #TODO: check that the name is short enough
        #TODO: check that the year makes sense
        pass

    def apply(self):
        """
        Saves the changes to the database.
        :return:
        """
        site_config = SiteConfiguration.instance()
        site_config.association_name = self.cleaned_data['name']
        site_config.association_contact_email = self.cleaned_data['contact_email']
        site_config.association_founded = self.cleaned_data['founded']
        site_config.save()


class ModulesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        Creates checkboxes for all labels in the keyword argument modules
        :param args:
        :param kwargs: modules: list of modules
        :return:
        """
        modules = kwargs.pop('modules')
        super(ModulesForm, self).__init__(*args, **kwargs)
        for module in modules:
            self.fields[module] = forms.BooleanField(label=module,
                                                     initial=DisabledModule.is_enabled(module),
                                                     required=False)

    def apply(self):
        """
        Saves the changes to the database.
        :return:
        """
        for module, enabled in self.cleaned_data.items():
            if module in settings.OPTIONAL_APPS:
                if enabled:
                    DisabledModule.enable(module)
                else:
                    DisabledModule.disable(module)




