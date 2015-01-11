from django import forms
from .models import Member, PaymentPurpose
from base.models import SiteConfiguration
from django.utils.translation import ugettext as _


class MemberApplicationForm(forms.ModelForm):
    member = forms.BooleanField(label=_("I am a member of this association"), initial=False, required=True)

    class Meta():
        model = Member
        fields = ('enrollment_year', 'graduation_year')

    def clean(self):
        super(MemberApplicationForm, self).clean()
        # Make sure that the enrollment and graduation years make sense
        enroll = self.cleaned_data['enrollment_year']
        graduate = self.cleaned_data['graduation_year']
        if enroll < SiteConfiguration.founded():
            self._errors['enrollment_year'] = _("You cannot have enrolled before the association was created.")
        if graduate:
            if graduate <= enroll:
                self._errors['graduation_year'] = _("You cannot have graduated before you enrolled")


class PaymentPurposeForm(forms.ModelForm):
    class Meta():
        model = PaymentPurpose
        fields = ('purpose', 'description')