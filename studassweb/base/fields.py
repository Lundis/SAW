from ckeditor_uploader.fields import RichTextUploadingField, RichTextUploadingFormField
from django import forms
from .html_tag_closer import complete_html
import re


class ValidatedRichTextField(RichTextUploadingField):
    """
    This class changes the default form field, to use a custom one that automatically closes HTML tags.
    """

    def formfield(self, **kwargs):
        # Change the default form field
        if 'form_class' not in kwargs:
            kwargs['form_class'] = ValidatedRichTextFormField
        return super().formfield(**kwargs)

    @staticmethod
    def get_summary(text, length):
        """
        Returns a summary with valid markup of approximately the requested length.
        :param length:
        :return:
        """
        html, closing_tags = complete_html(text[:length])
        summary = html + closing_tags
        return summary


class ValidatedRichTextFormField(RichTextUploadingFormField):

    def clean(self, value):
        """
        Closes any open tags on the value.
        Removes any trailing "<p>&nbsp;</p>" lines.
        :param value:
        :return:
        """
        cleaned = super().clean(value)
        html, closing_tags = complete_html(cleaned)
        return self.remove_trailing_stupid_lines(html + closing_tags)

    @staticmethod
    def remove_trailing_stupid_lines(text):
        lines = text.replace("\r", "").split("\n")
        good_line_found = False
        result = ""
        # iterate backwards through the lines
        for i in range(len(lines)-1, -1, -1):  # stop when at index -1
            if not lines[i].strip() in ("", "<p>&nbsp;</p>"):
                good_line_found = True
            if good_line_found:
                result = lines[i] + "\n" + result
        print("removed:\n" + text[len(result):])
        return result


class HiddenModelField(forms.IntegerField):
    """
    A menu field for interpreting the order of a model
    POST.field.name must be in the form *-<id>, where id is a valid id
    POST.field.value must be an integer >= 0
    """
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        model = kwargs.pop('model')
        super().__init__(*args, **kwargs)
        self.name = name
        self.model = model

    def clean(self, value):
        """

        :param value: The value attribute of the field
        :return: clean value
        """
        cleaned_num = super().clean(value)
        # Check that the id is positive and that the menu item actually exists
        if cleaned_num < 0:
            raise forms.ValidationError("Menu item index below 0")
        # assume that the form has only added proper fields,
        # so we only check that the last part of the name is a valid menu item id
        item_id = int(self.name.split('-')[-1])
        if self.model.objects.filter(id=item_id).count() != 1:
            raise forms.ValidationError("%s with id %d does not exist!", self.model, item_id)
        # else return the cleaned menu index
        return cleaned_num
    
    
class HiddenComponentClassField(forms.CharField):
    """
    A menu field for interpreting the order of a model
    POST.field.name must be in the form *-<id>, where id is a valid id
    POST.field.value must be an integer >= 0
    """
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        super().__init__(*args, **kwargs)
        self.name = name

    def clean(self, value):
        """

        :param value: The value attribute of the field
        :return: clean value
        """
        cleaned_css_classes = super().clean(value)
        if not re.match(r"^[a-zA-Z0-9\- ]*$", cleaned_css_classes):
            raise forms.ValidationError("Invalid character found")
        if len(cleaned_css_classes) > 250:
            raise forms.ValidationError("Classes string too long")

        return cleaned_css_classes
    