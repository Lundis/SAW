from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from base.models import SiteConfiguration, DisabledModule
from menu.models import MenuItem, Menu
from menu.fields import HiddenMenuField
import datetime

import re

# TODO for all forms: sanitize input according to the requirements / design.


class AssociationForm(forms.Form):
    name = forms.CharField(label=_('Association name'))
    founded = forms.IntegerField(label=_('Founded year'), min_value=0, max_value=datetime.datetime.now().year)

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = SiteConfiguration.instance().association_name
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
            self.fields[module] = forms.BooleanField(label=module, initial=DisabledModule.is_enabled(module), required=False)

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


# dynamic menu field and form: http://stackoverflow.com/questions/6154580/django-dynamic-form-example
class MenuForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Parses all hidden menu items.
        Their name attributes should start with "menu-item-" and their value should be the position of the menu item.
        :param args: request.POST or None
        :param kwargs:
        :return:
        """
        super(MenuForm, self).__init__(*args, **kwargs)
        if len(args) > 0 and args[0] != None:
            self.add_menu_fields(args[0])

    def add_menu_fields(self, post_data):
        for key, value in post_data.items():
            matches = re.match(r"^(main|login)-menu-item-(\d+)$", key)
            if matches and key not in self.fields.keys():
                self.fields[key] = HiddenMenuField(name=key, initial=value, required=True)

    def clean(self):
        self.cleaned_data['main_menu_items'] = []
        self.cleaned_data['login_menu_items'] = []
        for key, value in self.cleaned_data.items():
            matches = re.match(r"^(main|login)-menu-item-(\d+)$", key)

            if matches:
                if matches.group(1) == "main":
                    self.cleaned_data['main_menu_items'].append((int(matches.group(2)), value,))
                else:
                    self.cleaned_data['login_menu_items'].append((int(matches.group(2)), value,))

    def apply(self):
        """
        Saves the menu to the database. Will crash if run before is_valid().
        :return:
        """
        # get menus
        main_menu, created = Menu.get_or_create("main_menu")
        login_menu, created = Menu.get_or_create("login_menu")

        # clear them
        main_menu.clear()
        login_menu.clear()

        #fill with new values
        for menuitem, order in self.cleaned_data['main_menu_items']:
            menu_item = MenuItem.objects.get(id=menuitem)
            main_menu.add_item(menu_item, order)

        for menuitem, order in self.cleaned_data['login_menu_items']:
            login_item = MenuItem.objects.get(id=menuitem)
            login_menu.add_item(login_item, order)

