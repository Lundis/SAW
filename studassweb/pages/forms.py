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

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('user')
        super(InfoPageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        page = super(InfoPageForm, self).save(commit=False)
        page.author = self.author
        if commit:
            page.save()
        return page