from django import forms
from .models import Member, PaymentPurpose
from users.groups import GROUP_CHOICES, get_user_group, put_user_in_default_group
from django.utils.translation import ugettext as _


class MemberApplicationForm(forms.ModelForm):
    member = forms.BooleanField(label=_("I am a member of this association"), initial=False, required=True)

    class Meta():
        model = Member
        fields = ('enrollment_year', 'graduation_year')


class PaymentPurposeForm(forms.ModelForm):
    class Meta():
        model = PaymentPurpose
        fields = ('purpose', 'description')


class MemberEditForm(forms.ModelForm):
    group = forms.ChoiceField(GROUP_CHOICES, label=_("Group"))

    class Meta:
        model = Member
        fields = ("user_ext",
                  "first_name",
                  "last_name",
                  "email",
                  "enrollment_year",
                  "graduation_year",
                  "confirmed",
                  "can_apply_for_membership",)

    def __init__(self, *args, **kwargs):
        super(MemberEditForm, self).__init__(*args, **kwargs)
        # if this is an instance and the user hasn't already entered data
        if 'instance' in kwargs and not args[0]:
            instance = kwargs['instance']
            if instance is not None and instance.user_ext is not None:
                user = instance.user_ext.user
                self.fields['group'].initial = get_user_group(user)

    def save(self, commit=True):
        instance = super(MemberEditForm, self).save(commit)
        # update permissions if this user
        if instance.user_ext is not None:
            user = instance.user_ext.user
            put_user_in_default_group(user, self.cleaned_data['group'])
            if commit:
                user.save()
        return instance

