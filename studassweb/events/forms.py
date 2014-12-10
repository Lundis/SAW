__author__ = 'Olujuwon'
from django import forms
from django.forms import ModelForm
from events.models import EventSignup


class Eventsignup(forms.ModelForm):

    class Meta:
        model = EventSignup
        fields = ('title', 'body', 'creation', 'author')


class BlogeditForm(ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'body')