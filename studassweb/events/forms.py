from django import forms
from .models import Event, EventSignup


#TODO do we want to ask for name of logged-in users?
#Easiest would maybe be to autofill text field with username but allow user to change
class EventSignupForm(forms.ModelForm):

    class Meta:
        model = EventSignup
        fields = ('name', 'email', 'matricle', 'association', 'diet', 'other')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'text', 'start', 'stop', 'author', 'signup_deadline')

