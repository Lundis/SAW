from django import forms
# Here you want some form
# Google for inline formset https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets
# or look at install/forms.py, maybe easier
from polls.models import *
from django.utils.translation import ugettext_lazy as _


class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ('name', 'description', 'publication', 'expiration', 'can_vote_on_many')

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
        fields = ('name',)
        labels = {
            'name': _('Choice'),
            }


class ChoiceFormSingle(forms.Form):

    def __init__(self, *args, **kwargs):
        poll_choices = kwargs.pop("poll_choices")
        super(ChoiceFormSingle, self).__init__(*args, **kwargs)
        choices = ()
        for choice in poll_choices:
            choices += (str(choice.id), choice.name),
        self.fields["choices"] = forms.ChoiceField(choices=choices,
                                                   widget=forms.RadioSelect)

    def save(self, request, commit=True):
        if self.is_valid():
            choice_id = self.cleaned_data['choices']
            choice = Choice.objects.get(id=int(choice_id))

            if(request.user.is_authenticated()):
                user=request.user
            else:
                user=None
            vote = Votes(choice_id=choice,
                         user=user,
                         ip_address=request.META['REMOTE_ADDR'])
            if commit:
                vote.save()
            return vote

    class Meta:
        model = Choice
        fields = ('name',)
        labels = {
            'name': _('Choice'),
            }


class ChoiceFormMultiple(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        poll_choices = kwargs.pop("poll_choices")
        super(ChoiceFormSingle, self).__init__(*args, **kwargs)
        choices = ()
        for choice in poll_choices:
            choices += (str(choice.id), choice.name),
        self.fields["choices"] = forms.MultipleChoiceField(choices=choices)




    def save(self,request,poll,commit=True):
        if self.is_valid():
            ids_of_choices = self.cleaned_data["choices"]
            if(request.user.is_authenticated()):
                user=request.user
            else:
                user=None
            for id_choice in ids_of_choices:
                try:
                    choice = Choice.objects.get(id=id_choice)

                    vote = Votes(choice_id=choice,
                                 user=user,
                                 ip_address=request.META['REMOTE_ADDR'])
                    if(commit):
                        vote.save()
                except Choice.DoesNotExist:
                    raise  # TODO something
            return None


    class Meta:
        model = Choice
        fields = ('name',)
        labels = {
            'name': _('Choice'),
            }