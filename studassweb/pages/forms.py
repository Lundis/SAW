# coding=utf-8
from django import forms
from .models import InfoCategory, InfoPage


class InfoCategoryForm(forms.ModelForm):

    class Meta:
        model = InfoCategory
        fields = ("name", "permission")


class InfoPageForm(forms.ModelForm):

    class Meta:
        model = InfoPage
        fields = ("title", "text", "category", "permission", "for_frontpage")

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        page = super().save(commit=False)
        page.author = self.author
        if commit:
            page.save()
        return page
