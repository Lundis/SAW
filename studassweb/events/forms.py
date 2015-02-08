from django import forms
from .models import Event, EventSignup, EventItem, ItemInEvent, ItemInSignup
from datetime import date


#TODO do we want to ask for name of logged-in users?
#Easiest would maybe be to autofill text field with username but allow user to change
class EventSignupForm(forms.ModelForm):

    class Meta:
        model = EventSignup
        fields = ('name', 'email', 'matricle', 'association', 'diet', 'other')


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
        self.fields["eitems"] = forms.MultipleChoiceField(choices=eitems, initial=selected_eitems)

    def save(self, event):
        if self.is_valid():
            ids_of_event_items = self.cleaned_data['eitems']

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
        selected_eitems = []
        #if signup:
        #    selected_event_items = ItemInSignup.objects.filter(signup=signup)
        #    for tmp in selected_event_items:
        #        selected_eitems.append(tmp.item.id)
        super(SignupItemsForm, self).__init__(*args, **kwargs)
        this_event_items = []
        this_event_iteminevents = ItemInEvent.objects.filter(event=event)
        for iteminevent in this_event_iteminevents:
            this_event_items.append(iteminevent.item)
        eitems = ()
        i = 0
        for eitem in this_event_items:
            eitems += (str(eitem.id), eitem.name),
            self.fields["eitems-"+str(i)] = forms.CharField(label=eitem.name)
            i += 1

    def save(self, event):
        if self.is_valid():
            pass
            # TODO loop through everything starting with "eitems"
            # this should by the way be a constant
            # save every textfield as a ItemInSignup
