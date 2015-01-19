from django import forms
# Here you want some form
# Google for inline formset https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets
# or look at install/forms.py, maybe easier
from polls.models import *


class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ('name','description','publication','expiration')

    def save(self, commit=True, user=None):
        poll = super(PollForm, self).save(commit=False)
        if not hasattr(poll, "created_by") and user is not None:
            poll.created_by = user
        if commit:
            poll.save()
            # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            # So we need this method because we used commit=False earlier
            self.save_m2m()
        return poll


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('id_to_poll','name')