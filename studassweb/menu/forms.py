# coding=utf-8
from django import forms
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _
from .fields import HiddenMenuField
from .models import MenuItem, Menu, TYPE_USER, MainMenuSettings, MenuTemplate, TYPE_APP
import re
import logging

logger = logging.getLogger(__name__)

# dynamic menu field and form: http://stackoverflow.com/questions/6154580/django-dynamic-form-example


class MenuForm(forms.Form):
    """
    Parses all hidden menu items.
    Their name attributes should start with "menu-item-" and their value should be the position of the menu item.
    :param args: request.POST or None
    :param kwargs:
    :return:
    """
    def __init__(self, *args, menus=None, initial_items=None, available_items=None, **kwargs):
        """

        :param menus: a list of menus
        :param initial_items: a dict of items that will be rendered inside each menu
        :param available_items: the items that will be rendered as not belonging to a menu
        :return:
        """
        self.menus = menus
        self._verify_argument_menus()
        self.menus = {}
        for menu in menus:
            self.menus[menu.menu_name] = menu
        if initial_items:
            if not isinstance(initial_items, dict):
                raise ValueError("initial_items must be a dictionary")
        self.default_items = initial_items

        self.available_items = available_items
        super().__init__(*args, **kwargs)
        # the first argument is the post data
        if len(args) > 0 and args[0]:
            self.add_menu_fields(args[0])

    def _verify_argument_menus(self):
        """
        Verifies that the menus keyword argument was correct.
        :return:
        """
        if not self.menus:
            raise ValueError("required keyword argument 'menus' missing")
        menus_type = type(self.menus)
        if menus_type is not list and menus_type is not tuple:
            raise ValueError("menus must be a list or a tuple")
        for menu in self.menus:
            if not isinstance(menu, Menu):
                raise ValueError("item " + menu + " in menus is not a Menu")

    def add_menu_fields(self, post_data):
        menu_strings = self.menus.keys()
        menu_regex = '|'.join(menu_strings)
        for name, index in post_data.items():
            matches = re.match(r"^(" + menu_regex + ")-menu-item-(\d+)$", name)
            # if it's a match and it isn't a duplicate
            if matches and name not in self.fields.keys():
                self.fields[name] = HiddenMenuField(name=name, initial=index, required=True)

    def clean(self):
        menu_strings = self.menus.keys()
        for menu_string in menu_strings:
            self.cleaned_data[menu_string + '_menu_items'] = []

        menu_regex = '|'.join(menu_strings)
        for name, value in self.cleaned_data.items():
            matches = re.match(r"^(" + menu_regex + ")-menu-item-(\d+)$", name)

            if matches:
                menu = self.menus[matches.group(1)]
                self.cleaned_data[menu.menu_name + '_menu_items'].append((int(matches.group(2)), value,))

    def put_items_in_menus(self):
        for menu in self.menus.values():
            self._put_items_in_menu(menu)

    def _put_items_in_menu(self, menu):
        menu.clear()
        for menu_item, order in self.cleaned_data[menu.menu_name + '_menu_items']:
            menu_item = MenuItem.objects.get(id=menu_item)
            menu.add_item(menu_item, order)

    def render_javascript(self):
        """
        renders the required javascript for this form
        :return:
        """
        template = get_template("menu/menu_form.html")
        menu_strings = "[" + ", ".join(['"' + s + '"' for s in self.menus.keys()]) + "]"
        context = {'menu_strings': menu_strings,
                   'form_name': self.get_form_id()}
        result = template.render(Context(context))
        return result

    def rendered_menu_editors(self):
        """
        return a list of rendered menus
        :return:
        """
        menu_html = {}
        for menu_name, menu in self.menus.items():
            if self.default_items:
                items = self.default_items[menu_name]
            else:
                items = menu.items()
            menu_html[menu_name] = self._render_menu(menu_name, items)
        return menu_html

    @staticmethod
    def _render_menu(menu_name, menu_items):
        """
        renders the menu items of a menu
        :param menu_name:
        :param menu_items:
        :return:
        """

        template = get_template("menu/menu_editor.html")
        context = Context({'menu_name': menu_name,
                           'items': menu_items})
        result = template.render(context)
        return result

    def render_available_items(self):
        """
        renders the available menu items
        :return:
        """
        items = self.available_items
        return self._render_menu("available", items)

    @staticmethod
    def get_form_id():
        return "menu-editor-form"

    @staticmethod
    def get_submit_js():
        return "updateHiddenFormFields();"


class MenuCreationForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('menu_name',)

    def save(self, *args, **kwargs):
        new = not self.instance or not self.instance.pk
        menu = super().save(*args, **kwargs)
        menu.created_by = TYPE_USER
        menu.save()
        # Now create a menu item so that users can add it to other menus
        if new:
            MenuItem.objects.create(identifier="item_for_menu_%s" % menu.id,
                                    display_name=menu.menu_name,
                                    submenu=menu,
                                    created_by=TYPE_APP)
        return menu


class UserMenuItemForm(forms.ModelForm):
    """
    A form for creating and editing user-created menu items
    """
    class Meta:
        model = MenuItem
        fields = ('display_name',
                  'external_url',
                  'submenu',
                  'view_permission')

    def clean(self):
        super().clean()
        # We need to verify that that the user entered either an external url or a submenu
        # However, that is done by the model's clean() function automatically (woo!)

        # Next we need to check if the user put http:// in front of the url or not (this is required for it work)
        url = self.cleaned_data['external_url']
        if url is not None and len(url) > 0:
            if not url.startswith("http://") and not url.startswith("https://"):
                self.cleaned_data['external_url'] = "http://" + url

    def save(self, commit=True):
        new_item = not self.instance.pk
        item = super().save(commit=False)
        item.created_by = TYPE_USER
        if new_item:
            # find a unique identifier

            id = MenuItem.objects.filter(created_by=TYPE_USER).count() + 1
            while MenuItem.objects.filter(id=id, created_by=TYPE_USER).exists():
                id += 1
            logger.debug("Creating identifier for user-generated menu item. id %s" % id)
            item.identifier = "user-menu-item-%s" % id
        if commit:
            item.save()
        return item


class AppMenuItemForm(forms.ModelForm):
    """
    A form to edit menu items created by apps. Only the display_name can be edited
    """
    class Meta:
        model = MenuItem
        fields = ('display_name',
                  'view_permission',)


class MainMenuForm(forms.ModelForm):
    template = forms.ModelChoiceField(MenuTemplate.objects.filter(for_main_menu=True),
                                      required=True)

    class Meta:
        model = MainMenuSettings
        fields = ('image', 'inverted_style')
        labels = {
            'image': _("Header image"),
            'inverted_style': _("Invert the colors of the menu")
        }

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {'template': Menu.get("main_menu").template}
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        template = self.cleaned_data['template']
        if template.uses_image:
            if 'image' not in self.cleaned_data:
                raise forms.ValidationError(_("You need to specify an image for the requested layout"))

    def save(self, commit=True):
        menu_settings = super().save(commit)
        main_menu = Menu.get("main_menu")
        main_menu.template = self.cleaned_data['template']
        if commit:
            main_menu.save()
        return menu_settings
