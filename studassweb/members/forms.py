from django import forms
from .models import Member, PaymentPurpose, CustomField, Payment, CustomEntry
from users.groups import GROUP_CHOICES, get_user_group, put_user_in_standard_group
from django.utils.translation import ugettext as _
from django.utils import timezone


class MemberApplicationForm(forms.ModelForm):
    member = forms.BooleanField(label=_("I am a member of this association"), initial=False, required=True)

    class Meta():
        model = Member
        fields = ('enrollment_year', 'graduation_year')


class PaymentPurposeForm(forms.ModelForm):
    class Meta():
        model = PaymentPurpose
        fields = ('purpose', 'description')


class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ('name',)


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ("purpose", "date", "expires")

    def __init__(self, *args, **kwargs):
        self._member = kwargs.pop("member")
        self._user = kwargs.pop("user")
        super(PaymentForm, self).__init__(*args, **kwargs)
        # Use now as the default time of payment
        self.fields["date"].initial = timezone.now()

    def save(self, commit=True):
        payment = super(PaymentForm, self).save(commit=False)
        payment.member = self._member
        payment.created_by = self._user
        if commit:
            payment.save()
        return payment


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
        # Not required for validation
        self.fields['enrollment_year'].required = False
        # Should not add the required flag to the HTML
        self.fields['enrollment_year'].widget.is_required = False
        # Add all custom fields
        fields = CustomField.objects.all()
        for field in fields:
            f = forms.CharField(required=False,
                                widget=forms.Textarea(),
                                label=field.name)
            # Populate the field with existing data if this is an existing member
            if self.instance and self.instance.pk:
                entry, created = CustomEntry.objects.get_or_create(field=field,
                                                                   member=self.instance)
                f.initial = entry.content
            self.fields["custom-" + field.name] = f

    def save(self, commit=True):
        instance = super(MemberEditForm, self).save(commit)
        # update permissions if this user
        if instance.user_ext is not None:
            user = instance.user_ext.user
            put_user_in_standard_group(user, self.cleaned_data['group'])
            if commit:
                user.save()
        # Next save all custom fields
        fields = CustomField.objects.all()
        for field in fields:
            if commit:
                entry, created = CustomEntry.objects.get_or_create(field=field,
                                                          member=instance)
                entry.content = self.cleaned_data["custom-" + field.name]
                entry.save()

        return instance

