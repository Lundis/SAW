from django import forms
from django.core.validators import ValidationError
from .models import Event, EventSignup, EventItem, ItemInEvent, ItemInSignup
from base.utils import generate_email_ver_code

EITEMS = "eitems"


class EventSignupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        super(EventSignupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = EventSignup
        fields = ('name', 'email',)

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

    signup_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        input_formats=('%d.%m.%Y %H:%M',))

    class Meta:
        model = Event
        fields = ('title', 'text', 'signup_deadline', 'start', 'stop')

    def save(self, commit=True, user=None):
        if user is None:
            raise ValueError("Argument 'user' is missing")
        event = super(EventForm, self).save(commit=False)
        event.author = user
        if commit:
            event.save()
        return event


class EventItemsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event", None)
        selected_eitems = []
        if event:
            selected_event_items = ItemInEvent.objects.filter(event=event)
            for tmp in selected_event_items:
                selected_eitems.append(tmp.item.id)
        super(EventItemsForm, self).__init__(*args, **kwargs)
        all_event_items = EventItem.objects.filter()
        eitems = ()
        for eitem in all_event_items:
            eitems += (str(eitem.id), eitem.name),
        self.fields[EITEMS] = forms.MultipleChoiceField(choices=eitems, initial=selected_eitems, required=False)

    def save(self, event):
        if self.is_valid():
            ids_of_event_items = self.cleaned_data[EITEMS]

            # Let's remove all choices from this event
            ItemInEvent.objects.filter(event=event).delete()

            #  and then add them again!
            for id_ei in ids_of_event_items:
                try:
                    even_item = EventItem.objects.get(id=id_ei)
                    ItemInEvent(event=event, item=even_item).save()
                except EventItem.DoesNotExist:
                    raise  # TODO something
            return None


class SignupItemsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        signup = kwargs.pop("signup", None)
        selected_eitems = {}
        if signup:
            selected_signup_items = ItemInSignup.objects.filter(signup=signup)
            for signup_item in selected_signup_items:
                selected_eitems[signup_item.item.id] = signup_item.value
        super(SignupItemsForm, self).__init__(*args, **kwargs)
        this_event_items = []
        this_event_iteminevents = ItemInEvent.objects.filter(event=event)
        for iteminevent in this_event_iteminevents:
            this_event_items.append(iteminevent.item)
        for eitem in this_event_items:
            if eitem.type == EventItem.TYPE_BOOL:
                self.fields[EITEMS+str(eitem.id)] = forms.BooleanField(
                    label=eitem.name,
                    initial=selected_eitems.get(eitem.id),
                    required=eitem.required
                )
            elif eitem.type == EventItem.TYPE_STR:
                self.fields[EITEMS+str(eitem.id)] = forms.CharField(
                    label=eitem.name,
                    initial=selected_eitems.get(eitem.id),
                    required=eitem.required
                )
            elif eitem.type == EventItem.TYPE_TEXT:
                self.fields[EITEMS+str(eitem.id)] = forms.CharField(
                    widget=forms.Textarea,
                    label=eitem.name,
                    initial=selected_eitems.get(eitem.id),
                    required=eitem.required
                )
            elif eitem.type == EventItem.TYPE_INT:
                self.fields[EITEMS+str(eitem.id)] = forms.IntegerField(
                    label=eitem.name,
                    initial=selected_eitems.get(eitem.id),
                    required=eitem.required
                )
            elif eitem.type == EventItem.TYPE_CHOICE:
                # This will probably change...
                # Anyway, strings are splitted by //
                # First string is the label, rest is choices
                items = ()
                i = 0
                strings = eitem.name.split("//")
                for string in strings:
                    if i != 0:
                        items += (string, string),
                    i += 1
                self.fields[EITEMS+str(eitem.id)] = forms.ChoiceField(
                    choices=items,
                    label=strings[0],
                    initial=selected_eitems.get(eitem.id),
                    required=eitem.required
                )

    def save(self, signup):
        if self.is_valid():
            # Remove old
            ItemInSignup.objects.filter(signup=signup).delete()
            # Add new
            for index in self.cleaned_data:
                if str(index).startswith(EITEMS):
                    id1 = str(index)[len(EITEMS):]
                    event_item = EventItem.objects.get(id=id1)
                    tmp = ItemInSignup()
                    tmp.item = event_item
                    tmp.signup = signup
                    tmp.value = self.cleaned_data[index]
                    tmp.save()