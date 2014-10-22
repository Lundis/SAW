from django import forms
from django.utils.translation import ugettext as _
from base.models import SiteConfiguration, DisabledModule

# TODO for all forms: sanitize input according to the requirements / design.

class AssociationForm(forms.Form):
    name = forms.CharField(label=_('Association name'), initial=SiteConfiguration.instance().association_name)

class ModulesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        modules = kwargs.pop('modules')
        print(modules)
        super(ModulesForm, self).__init__(*args, **kwargs)
        for module in modules:
            self.fields[module] = forms.BooleanField(label=module, initial=DisabledModule.is_enabled(module))
            self.fields[module].widget = forms.CheckboxInput(attrs={'class': 'checkbox'})

class MenuForm(forms.Form):
    pass