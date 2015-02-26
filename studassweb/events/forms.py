from django import forms
from django.core.validators import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext as _
from .models import Event, EventSignup, EventItem, ItemInEvent, ItemInSignup
from base.utils import generate_email_ver_code
from captcha.fields import ReCaptchaField

EITEMS = "eitems"


class EventSignupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        self.user = kwargs.pop('user')
        super(EventSignupForm, self).__init__(*args, **kwargs)
        if self.event.use_captcha and not self.user.is_authenticated():
            self.fields['captcha'] = ReCaptchaField()

    class Meta:
        model = EventSignup
        fields = ('name', 'email')

    def clean(self):
        super(EventSignupForm, self).clean()
        if self.event.is_past_signup_deadline():
            raise ValidationError("It's already past the deadline!")

    def save(self, commit=True, user=None,):
        temp_signup = super(EventSignupForm, self).save(commit=False)
        temp_signup.event = self.event
        temp_signup.auth_code = generate_email_ver_code()
        while EventSignup.objects.filter(auth_code=temp_signup.auth_code).exists():
            temp_signup.auth_code = generate_email_ver_code()
        if not user.is_anonymous():
            temp_signup.user = user
        if commit:
            temp_signup.save()
        return temp_signup


class EventForm(forms.ModelForm):

    start = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        input_formats=('%d.%m.%Y %H:%M',))

    stop = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        input_formats=('%d.%m.%Y %H:%M',))

    signup_start = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        input_formats=('%d.%m.%Y %H:%M',),
        initial=timezone.now())

    signup_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        input_formats=('%d.%m.%Y %H:%M',))

    class Meta:
        model = Event
        fields = ('title', 'text', 'max_participants', 'signup_start', 'signup_deadline', 'start', 'stop', 'permission',
                  'use_captcha', 'send_email_for_reserves'
                  )

    def clean(self):
        super(EventForm, self).clean()
        if self.cleaned_data['signup_start'] > self.cleaned_data['signup_deadline']:
            self.add_error('signup_deadline', _("The signup deadline can't be before it starts"))

        if self.cleaned_data['start'] > self.cleaned_data['stop']:
            self.add_error('stop', _("The event can't end before it starts!"))

    def save(self, commit=True, user=None):
        if user is None:
            raise ValueError("Argument 'user' is missing")
        event = super(EventForm, self).save(commit=False)
        event.author = user
        if commit:
            event.save()
        return event


class EventItemsForm(forms.Form):
    """
    A form for creating/editing event items
    That is, the event items which are used in a specific event.
    """
    def __init__(self, *args, **kwargs):
        # If editing, keep track of items already applied to event so we can mark them as applied in the form.
        event = kwargs.pop("event", None)
        selected_eitems = []
        if event:
            selected_event_items = ItemInEvent.objects.filter(event=event)
            for tmp in selected_event_items:
                selected_eitems.append(tmp.item.id)

        super(EventItemsForm, self).__init__(*args, **kwargs)

        all_event_items = EventItem.objects.filter()
        # Create a 'choices' variable with all event items, in the right format
        choices_eitems = ()
        for eitem in all_event_items:
            choices_eitems += (str(eitem.id), eitem.name),

        self.fields[EITEMS] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            choices=choices_eitems,
            initial=selected_eitems,
            required=False,
            label=_("Event items"),
            help_text=_("Event items are optional signup fields for an event.")
        )

    def clean(self):
        super(EventItemsForm, self).clean()
        ids_of_event_items = self.cleaned_data[EITEMS]
        # Check that all event items added to event exists
        for id_ei in ids_of_event_items:
                try:
                    EventItem.objects.get(id=id_ei)
                except EventItem.DoesNotExist:
                    self.add_error(EITEMS, _("Tried to add nonexistant event item"))

    def save(self, event):
        if self.is_valid():
            ids_of_event_items = self.cleaned_data[EITEMS]

            # Let's remove all chosen event items from this event
            ItemInEvent.objects.filter(event=event).delete()

            #  and then create/add the newly chosen ones!
            for id_ei in ids_of_event_items:
                even_item = EventItem.objects.get(id=id_ei)
                ItemInEvent(event=event, item=even_item).save()
            return None


class SignupItemsForm(forms.Form):
    """
    A form for selecting items in a signup form
    """
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        signup = kwargs.pop("signup", None)
        selected_eitems = {}
        # If we are editing an existing signup, we need to get the old event item values to show in forms
        if signup:
            selected_signup_items = ItemInSignup.objects.filter(signup=signup)
            for signup_item in selected_signup_items:
                selected_eitems[signup_item.item.id] = signup_item.value

        super(SignupItemsForm, self).__init__(*args, **kwargs)

        # So every field's id is (static string for event items)+(id for the event item)
        # The static string in the beginning is to ensure we are not mixing form inputs or anything similar.
        for item_in_event in ItemInEvent.objects.filter(event=event):
            if item_in_event.item.type == EventItem.TYPE_BOOL:
                self.fields[EITEMS+str(item_in_event.item.id)] = forms.BooleanField(
                    label=item_in_event.item.name,
                    initial=selected_eitems.get(item_in_event.item.id),
                    required=item_in_event.item.required
                )
            elif item_in_event.item.type == EventItem.TYPE_STR:
                self.fields[EITEMS+str(item_in_event.item.id)] = forms.CharField(
                    label=item_in_event.item.name,
                    initial=selected_eitems.get(item_in_event.item.id),
                    required=item_in_event.item.required
                )
            elif item_in_event.item.type == EventItem.TYPE_TEXT:
                self.fields[EITEMS+str(item_in_event.item.id)] = forms.CharField(
                    widget=forms.Textarea,
                    label=item_in_event.item.name,
                    initial=selected_eitems.get(item_in_event.item.id),
                    required=item_in_event.item.required
                )
            elif item_in_event.item.type == EventItem.TYPE_INT:
                self.fields[EITEMS+str(item_in_event.item.id)] = forms.IntegerField(
                    label=item_in_event.item.name,
                    initial=selected_eitems.get(item_in_event.item.id),
                    required=item_in_event.item.required
                )
            elif item_in_event.item.type == EventItem.TYPE_CHOICE:
                # This will probably change...
                # Anyway, strings are splitted by //
                # First string is the label, rest is choices
                items = ()
                i = 0
                strings = item_in_event.item.name.split("//")
                for string in strings:
                    if i != 0:
                        items += (string, string),
                    i += 1
                self.fields[EITEMS+str(item_in_event.item.id)] = forms.ChoiceField(
                    choices=items,
                    label=strings[0],
                    initial=selected_eitems.get(item_in_event.item.id),
                    required=item_in_event.item.required
                )

    def save(self, signup):
        if self.is_valid():
            # Remove old event items for event
            ItemInSignup.objects.filter(signup=signup).delete()
            # Add newly selected. The field's ids' ends with the event item id
            for index in self.cleaned_data:
                if str(index).startswith(EITEMS):
                    id1 = str(index)[len(EITEMS):]
                    event_item = EventItem.objects.get(id=id1)
                    tmp = ItemInSignup()
                    tmp.item = event_item
                    tmp.signup = signup
                    tmp.value = self.cleaned_data[index]
                    tmp.save()