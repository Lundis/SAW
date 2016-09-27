# coding=utf-8
from django import forms
from django.core.validators import ValidationError
from django.utils.translation import ugettext as _
from .models import FrontPageItem
import logging

logger = logging.getLogger(__name__)


class PlacementForm(forms.ModelForm):
    item_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = FrontPageItem
        fields = ("ordering_index", "location")

    def clean_item_id(self):
        try:
            FrontPageItem.objects.get(id=self.cleaned_data['item_id'])
            return self.cleaned_data['item_id']
        except FrontPageItem.DoesNotExist:
            raise ValidationError(_("The specified frontpage item does not exist"))

    def save(self, commit=True):
        if self.is_valid():
            item = FrontPageItem.objects.get(id=self.cleaned_data['item_id'])
            item.location = self.cleaned_data['location']
            item.ordering_index = self.cleaned_data['ordering_index']
            if commit:
                item.save()
