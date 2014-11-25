from django import forms
from .models import InfoCategory, InfoPage


class InfoCategoryForm(forms.ModelForm):

    class Meta:
        model = InfoCategory
        fields = ("name", "permission")


class InfoPageForm(forms.ModelForm):

    class Meta:
        model = InfoPage
        fields = ("title", "text", "category", "permission")

