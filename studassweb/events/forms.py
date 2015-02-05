from django import forms
from .models import Event, EventSignup
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

