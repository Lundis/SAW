from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from base.models import SiteConfiguration, DisabledModule

# TODO for all forms: sanitize input according to the requirements / design.

class AssociationForm(forms.Form):
    name = forms.CharField(label=_('Association name'))

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = SiteConfiguration.instance().association_name

    def clean(self):
        #TODO: check that the name is short enough
        pass

    def Apply(self):
        """
        Saves the changes to the database.
        :return:
        """
        site_config = SiteConfiguration.instance()
        site_config.association_name = self.cleaned_data['name']
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
            self.fields[module] = forms.BooleanField(label=module, initial=DisabledModule.is_enabled(module), required=False)

    def Apply(self):
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

class MenuForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Parses all hidden menu items.
        Their name attributes should start with "menu-item-" and their value should be the position of the menu item.
        :param args:
        :param kwargs:
        :return:
        """
        super(MenuForm, self).__init__(*args, **kwargs)

