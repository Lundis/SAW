from django import forms
from .fields import HiddenMenuField
from .models import MenuItem
import re

# dynamic menu field and form: http://stackoverflow.com/questions/6154580/django-dynamic-form-example


class MenuForm(forms.Form):
    """
    Parses all hidden menu items.
    Their name attributes should start with "menu-item-" and their value should be the position of the menu item.
    :param args: request.POST or None
    :param kwargs:
    :return:
    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: must contain menus, which is a list or tuples tuples of alphabetic letters
        :return:
        """
        self.menus = kwargs.pop('menus')
        self.verify_argument_menus()
        super(MenuForm, self).__init__(*args, **kwargs)
        # the first argument is the post data
        if len(args) > 0 and args[0]:
            self.add_menu_fields(args[0])

    def verify_argument_menus(self):
        """
        Verifies that the menus keyword argument was correct.
        :return:
        """
        if not self.menus:
            raise ValueError("required keyword argument 'menus' missing")
        menus_type = type(self.menus)
        if not menus_type is list and not menus_type is tuple:
            raise ValueError("menus must be a list or a tuple")
        for menu in self.menus:
            if not isinstance(menu, str):
                raise ValueError("item " + menu + " in menus is not a string")
            if not re.match(r'^[a-zA-Z]+$', menu):
                raise ValueError("item " + menu + " contains non-alphabetic characters")

    def add_menu_fields(self, post_data):
        menu_regex = '|'.join(self.menus)
        for name, index in post_data.items():
            matches = re.match(r"^(" + menu_regex + ")-menu-item-(\d+)$", name)
            # if it's a match and it isn't a duplicate
            if matches and name not in self.fields.keys():
                self.fields[name] = HiddenMenuField(name=name, initial=index, required=True)

    def clean(self):
        for menu in self.menus:
            self.cleaned_data[menu + '_menu_items'] = []
        menu_regex = '|'.join(self.menus)
        for name, value in self.cleaned_data.items():

            matches = re.match(r"^(" + menu_regex + ")-menu-item-(\d+)$", name)

            if matches:
                menu = self.menus[self.menus.index(matches.group(1))]
                self.cleaned_data[menu + '_menu_items'].append((int(matches.group(2)), value,))

    def put_items_in_menu(self, menu_string, menu):
        if menu_string not in self.menus:
            raise ValueError("the specified menu identifier (" + menu_string + ") is not in " + self.menus)
        menu.clear()
        for menuitem, order in self.cleaned_data[menu_string + '_menu_items']:
            menu_item = MenuItem.objects.get(id=menuitem)
            menu.add_item(menu_item, order)