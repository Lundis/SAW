from django import forms
from menu.models import MenuItem


class HiddenMenuField(forms.IntegerField):
    """
    A menu field for interpreting the order of a menu item
    POST.field.name must be in the form *-<id>, where id is a valid menu id
    POST.field.value must be an integer >= 0
    """
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super(HiddenMenuField, self).__init__(*args, **kwargs)
        self.name = name

    def clean(self, value):
        """

        :param value: The value attribute of the field
        :return: clean value
        """
        cleaned_num = super(HiddenMenuField, self).clean(value)
        # Check that the id is positive and that the menu item actually exists
        if cleaned_num < 0:
            raise forms.ValidationError("Menu item index below 0")
        # assume that the form has only added proper fields,
        # so we only check that the last part of the name is a valid menu item id
        menu_item_index = int(self.name.split('-')[-1])
        if MenuItem.objects.filter(id=menu_item_index).count() != 1:
            raise forms.ValidationError("Menu item " + menu_item_index + " does not exist! You h4x0r!!")
        # else return the cleaned menu index
        return cleaned_num