from django import forms
from django.core.validators import ValidationError
# Here you want some form
# Google for inline formset https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets
# or look at install/forms.py, maybe easier
from polls.models import Poll, Choice, Vote
from django.utils.translation import ugettext_lazy as _


class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ('title', 'description', 'expiration',
                  'can_vote_on_many', "permission_choice_view", "permission_choice_vote")

    def save(self, commit=True, user=None):
        poll = super().save(commit=False)
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

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.strip() == "":
            raise ValidationError("A choice cannot be empty")


class ChoiceFormSingle(forms.Form):

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop("poll")
        poll_choices = kwargs.pop("poll_choices")
        super().__init__(*args, **kwargs)
        choices = ()
        for choice in poll_choices:
            choices += (str(choice.id), choice.name),
        self.fields["choices"] = forms.ChoiceField(choices=choices,
                                                   widget=forms.RadioSelect)

    def clean_choices(self):
        choice_id = self.cleaned_data['choices']
        choice = Choice.objects.get(id=int(choice_id))
        if choice.id_to_poll != self.poll:
            raise ValidationError("Selected choice is not in poll")
        return choice_id

    def save(self, request, commit=True):
        if self.is_valid():
            choice_id = self.cleaned_data['choices']
            choice = Choice.objects.get(id=int(choice_id))

            if request.user.is_authenticated():
                user = request.user
            else:
                user = None
            vote = Vote(choice_id=choice,
                        user=user,
                        ip_address=request.META['REMOTE_ADDR'])
            if commit:
                vote.save()
            return vote

    class Meta:
        model = Choice
        fields = ('name',)


class ChoiceFormMultiple(forms.Form):

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop("poll")
        poll_choices = kwargs.pop("poll_choices")
        super().__init__(*args, **kwargs)
        choices = ()
        for choice in poll_choices:
            choices += (str(choice.id), choice.name),
        self.fields["choices"] = forms.MultipleChoiceField(choices=choices,
                                                           widget=forms.CheckboxSelectMultiple)

    def clean_choices(self):
        choice_id = self.cleaned_data['choices']
        for c in choice_id:
            try:
                choice = Choice.objects.get(id=int(c))
                if choice.id_to_poll != self.poll:
                    raise ValidationError("Selected choice is not in poll")
            except Choice.DoesNotExist:
                raise ValidationError("Selected choice(s) do not exist!?")
        return choice_id

    def save(self, request, commit=True):
        if self.is_valid():
            ids_of_choices = self.cleaned_data["choices"]
            if request.user.is_authenticated():
                user = request.user
            else:
                user = None
            votes = ()
            for id_choice in ids_of_choices:
                choice = Choice.objects.get(id=id_choice)

                vote = Vote(choice_id=choice,
                            user=user,
                            ip_address=request.META['REMOTE_ADDR'])
                if commit:
                    vote.save()
                votes += (vote,)
            return votes
