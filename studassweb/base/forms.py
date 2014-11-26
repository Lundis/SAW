from django import forms


class ConfirmationForm(forms.Form):
    confirmation_box = forms.BooleanField(widget=forms.CheckboxInput, required=True)