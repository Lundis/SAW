from django import forms
from django.forms import ValidationError
from django.forms.widgets import Textarea
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import SuspiciousOperation
from .models import SiteConfiguration, BootswatchTheme, Feedback, \
    CSSOverrideFile, CSSOverrideContent, CSSMap2
from .fields import HiddenModelField
from string import ascii_letters, digits
import re


class DummyForm(forms.Form):
    """
    A form for when you only need to check the CSRF token
    """
    pass


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
            BootswatchTheme.objects.get(name=theme_name)
        except BootswatchTheme.DoesNotExist:
            raise ValidationError("Theme " + theme_name + " does not exist")

    def save(self):
        settings = SiteConfiguration.instance()
        theme = BootswatchTheme.objects.get(name=self.cleaned_data['theme'])
        settings.bootstrap_theme_url = theme.bs_css_url
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
    def __init__(self, *args, container_model=None, child_model=None,
                 containers=None, initial_items=None, available_items=None, all_items=None, **kwargs):
        """
        :param args: request.POST or None
        :param container_model: The model representing the container (Such as Menu, Group)
        :param child_model: The model representing the items being sorted (Such as MenuItem, SAWPermission)
        :param containers: a dict of container identifiers (strings key)
                           and actual container objects (container_model)
        :param initial_items: a dict of an item sequence {"container_string": (item1, item2, ...)}
                              that will be
        :param available_items: an iterable of the items that will be rendered as not belonging to any specific container
        :return:
        """
        if len(args) > 0:
            post_items = args[0]
        else:
            post_items = None
        self.containers = containers
        self.container_model = container_model
        self.child_model = child_model
        if initial_items is None:
            self.items = {}
        else:
            self.items = initial_items
        self._available_items = available_items
        self.all_items = all_items
        self._verify_arguments()
        if initial_items is not None:
            self._add_indices()
        super(SortingForm, self).__init__(*args, **kwargs)
        # the first argument is the post data
        if post_items is not None:
            # Use post data to populate items if it's provided
            self._interpret_post_data(args[0])

    def _add_indices(self):
        """
        User-supplied data won't have indices, so we add them
        :return:
        """
        for container, items in self.items.items():
            wrapped_items = ()
            index = 0
            for item in items:
                wrapped_items += (item, index),
                index += 1
            self.items[container] = wrapped_items

    def _verify_arguments(self):
        """
        Verifies that the menus keyword argument was correct. Since this form is so complicated, I do this to
        make using/debugging it easier in the future.
        :return:
        """
        if self.container_model is None:
            raise ValueError("required keyword argument 'container_model' is missing")
        if self.child_model is None:
            raise ValueError("required keyword argument 'child_model' is missing")
        # Check that the container exists and contains the correct model
        if self.containers is None:
            raise ValueError("required keyword argument 'containers' is missing")
        if type(self.containers) != dict:
            raise ValueError("container must be a dictionary ({'container_name': container_object})")
        for c in self.containers.values():
            if not isinstance(c, self.container_model):
                raise ValueError("%s in containers is not a %s" % (str(c), str(self.container_model)))

        if not isinstance(self.items, dict):
            raise ValueError("initial_items must be a dictionary")
        # check that self.items contain lists for all containers
        for c in self.containers:
            if c not in self.items:
                # if not, create it
                self.items[c] = ()
        # check that all items are in a valid container and that they are indeed objects of class child_model
        for key, items_in_container in self.items.items():
            if key not in self.containers.keys():
                raise ValueError("key '%s' is not in containers" % key)
            for item in items_in_container:
                if not isinstance(item, self.child_model):
                    raise ValueError("item {0} in container {1} is not a {3}" % (str(item), key, self.child_model))

        # TODO: verify that all items are in self.all_items

    def _interpret_post_data(self, post_data):
        """
        Adds user-submitted data to self.fields
        :param post_data: a bunch of <container>-item-<id>=<index>
        :return:
        """
        container_strings = self.containers.keys()
        container_regex = '|'.join(container_strings)
        for name, index in post_data.items():
            matches = re.match(r"^(" + container_regex + ")-item-(\d+)$", name)
            # If it's a relevant entry (there are also stuff like csrf-tokens)
            # and it isn't a duplicate
            if matches and name not in self.fields.keys():
                # Add the field
                self.fields[name] = HiddenModelField(name=name, model=self.child_model, initial=index, required=True)
        self._update_available_items()

    def _update_available_items(self):
        """
        Puts all items that aren't in any container in self.items into self.available_items
        :return:
        """
        # clear available items
        self._available_items = ()
        # Then add any item not in any of the containers to it
        for item in self.all_items:
            if not self._is_item_in_items(item):
                self._available_items += item,

    def _is_item_in_items(self, item):
        for items_and_indices in self.items.values():
            if item in (item_and_index[0] for item_and_index in items_and_indices):
                return True
        return False

    def clean(self):
        # Super cleans the individual fields using HiddenModelField's validation
        super(SortingForm, self).clean()
        # We organize the resulting data into self.items
        containers_strings = self.containers.keys()
        container_regex = '|'.join(containers_strings)
        # Clear all containers in items
        for c in self.items:
            self.items[c] = ()
        # for all post data that matches the valid format
        used_ids = ()
        used_indices = {}
        for c in self.containers:
            used_indices[c] = ()

        for name, value in self.cleaned_data.items():
            matches = re.match(r"^(" + container_regex + ")-item-(\d+)$", name)
            if matches:
                # Add it to the correct item container
                container = matches.group(1)
                id = matches.group(2)
                index = value
                # Check for duplicates/tampering
                if id in used_ids:
                    self.add_error(None, "id %s appeared twice!" % id)
                    continue
                if index in used_indices[container]:
                    self.add_error(None, "index %s appeared twice in %s!" % (id, container))
                    continue
                # Add a tuple (item_id, index) to the container list
                item = self.child_model.objects.get(id=id)
                self.items[container] += (item, index),
                used_ids += id,
                used_indices[container] += index,
        self._update_available_items()

    def save(self):
        raise NotImplementedError("You need to subclass to use save()." +
                                  "Alternatively just read form.items and save it accordingly!")

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

    def cleaned_items(self):
        """
        Returns a dictionary:
            {'container_name': Group,
                               ({'item': item,
                                 'id': html_id},
                                ...,
                               )
             ...
            }
        :return:
        """
        items = {}
        for c in self.containers:
            items_in_container = ()
            for item in self.items[c]:
                items_in_container += {'item': item[0],
                                       'id': "item-" + str(item[0].id)},
            items[c] = self.containers[c], items_in_container
        return items

    def available_items(self):
        """
        renders the available items (those that aren't in any category) in the form
        ( {'item': item, 'id': html-id}, ... )
        :return:
        """
        items = self._available_items
        list_of_items = ()
        for item in items:
            list_of_items += {'item': item,
                              'id': "item-" + str(item.id)},
        return list_of_items

    @staticmethod
    def get_form_id():
        return "sorting-form"

    @staticmethod
    def get_submit_js():
        return "updateSortingFields();"


class CSSOverrideFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CSSOverrideFileForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = Textarea(attrs={'cols': '80', 'rows': '5'})

    class Meta:
        model = CSSOverrideFile
        fields = ("name", "description")

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise ValidationError("Name must be atleast 5 letters")
        if not all(c in ascii_letters + digits + ' ' for c in name):
            raise ValidationError("Name can only contain alphanumeric letters and spaces")

        if all(c == ' ' for c in name):
            raise ValidationError("Name cannot only be spaces")
        return name


class CSSOverrideContentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CSSOverrideContentForm, self).__init__(*args, **kwargs)
        self.fields['css'].widget = Textarea(attrs={'cols': '80', 'rows': '30'})

    class Meta:
        model = CSSOverrideContent
        fields = ("css",)

    def save(self, user=None, file=None, commit=True):
        instance = super(CSSOverrideContentForm, self).save(commit=False)
        instance.file = file
        instance.author = user
        if commit:
            instance.save()
        return instance


class CSSClassForm(forms.ModelForm):

    class Meta:
        model = CSSMap2
        fields = "value",

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.default_has_changed = False

        if not instance.pk:
            raise SuspiciousOperation("Someone tried to manually create a CSS Class")

        if commit:
            instance.save()
        return instance
