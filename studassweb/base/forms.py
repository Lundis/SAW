from django import forms
from django.forms import ValidationError
from django.template.loader import get_template
from django.template import Context
from .models import SiteConfiguration, BootswatchTheme, Feedback
from .fields import HiddenModelField
import re


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


class SortingForm(forms.Form):
    """
    A form that parses hidden items from a sorting page (such as the menu editor).
    """
    def __init__(self, *args, container_model=None, child_model=None, containers=None, initial_items=None, available_items=None, **kwargs):
        """
        :param args: request.POST or None
        :param model: The model representing the items being sorted
        :param categories: a list of category identifiers
        :param initial_items: a dict of items that will be rendered inside each container
        :param available_items: the items that will be rendered as not belonging to any specific container
        :return:
        """
        self.containers = containers
        self.container_model = container_model
        self.child_model = child_model
        self.default_items = initial_items
        self.available_items = available_items
        self._verify_arguments()
        super(SortingForm, self).__init__(*args, **kwargs)
        # the first argument is the post data
        if len(args) > 0 and args[0]:
            self.add_fields(args[0])

    def _verify_arguments(self):
        """
        Verifies that the menus keyword argument was correct.
        :return:
        """
        if self.model is None:
            raise ValueError("required keyword argument 'model' is missing")
        if self.categories is None:
            raise ValueError("required keyword argument 'categories' is missing")
        menus_type = type(self.menus)
        if self.default_items:
            if not isinstance(self.default_items, dict):
                raise ValueError("initial_items must be a dictionary")
        # TODO: verify that all the default items are of the correct type
        if not menus_type is dict:
            raise ValueError("keyword argument 'containers' must be a dictionary")
        for c in self.containers:
            if not isinstance(c, self.model):
                raise ValueError("%s in containers is not a %s" % (str(c), str(self.model)))

    def add_fields(self, post_data):
        """
        Adds user-submitted data to self.fields
        :param post_data: a bunch of <container>-item-<id>=<index>
        :return:
        """
        container_strings = self.containers.keys()
        container_regex = '|'.join(container_strings)
        for name, index in post_data.items():
            matches = re.match(r"^(" + container_regex + ")-item-(\d+)$", name)
            # if it's a match and it isn't a duplicate
            if matches and name not in self.fields.keys():
                self.fields[name] = HiddenModelField(name=name, model=self.child_model, initial=index, required=True)

    def clean(self):
        # Super cleans the individual fields using HiddenModelField's validation
        super(SortingForm, self).clean()
        # We organize the resulting data
        containers_strings = self.containers.keys()
        for container_str in containers_strings:
            # Create an empty list for each container
            self.cleaned_data[container_str + '_items'] = []

        container_regex = '|'.join(containers_strings)
        for name, value in self.cleaned_data.items():
            matches = re.match(r"^(" + container_regex + ")-item-(\d+)$", name)
            # if it matches the container
            if matches:
                # Add a tuple (item_id, index) to the container list
                self.cleaned_data[matches.group(1) + '_items'].append((int(matches.group(2)), value,))

    def save(self):
        raise NotImplementedError("You need to subclass save()!")

    def render_javascript(self):
        """
        renders the required javascript for this form
        :return:
        """
        template = get_template("base/sorting/sorting_form_JS.html")
        container_strings = "[" + ", ".join(['"' + s + '"' for s in self.containers.keys()]) + "]"
        context = {'container_strings': container_strings,
                   'form_name': self.get_form_id()}
        result = template.render(Context(context))
        return result

    def rendered_menu_editors(self):
        """
        return a dictionary of rendered containers
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

    def get_form_id(self):
        return "%s-editor-form" % self.model

    @staticmethod
    def get_submit_js():
        return "updateSortingFields();"