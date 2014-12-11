from django import forms
# Here you want some form
# Google for inline formset https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets
# or look at install/forms.py, maybe easier
from polls.models import *


class PollForm(forms.ModelForm):

    class Meta:
       model = Poll
       fields = ('name')


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('id_to_poll','name')