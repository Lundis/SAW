from django import forms
from django.utils.translation import ugettext as _

# TODO for all forms: sanitize input according to the requirements / design.

class AssociationForm(forms.Form):
    name = forms.CharField(label=_('Association name'))
