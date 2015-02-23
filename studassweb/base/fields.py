from ckeditor.fields import RichTextField, RichTextFormField
from django import forms
from .html_tag_closer import complete_html


class ValidatedRichTextField(RichTextField):
    """
    This class changes the default form field, to use a custom one that automatically closes HTML tags.
    """

    def formfield(self, **kwargs):
        # Change the default form field
        if 'form_class' not in kwargs:
            kwargs['form_class'] = ValidatedRichTextFormField
        return super(ValidatedRichTextField, self).formfield(**kwargs)

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


class ValidatedRichTextFormField(RichTextFormField):

    def clean(self, value):
        """
        Closes any open tags on the value.
        :param value:
        :return:
        """
        cleaned = super(ValidatedRichTextFormField, self).clean(value)
        html, closing_tags = complete_html(cleaned)
        return html + closing_tags


class HiddenModelField(forms.IntegerField):
    """
    A menu field for interpreting the order of a model
    POST.field.name must be in the form *-<id>, where id is a valid id
    POST.field.value must be an integer >= 0
    """
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        model = kwargs.pop('model')
        super(HiddenModelField, self).__init__(*args, **kwargs)
        self.name = name
        self.model = model

    def clean(self, value):
        """

        :param value: The value attribute of the field
        :return: clean value
        """
        cleaned_num = super(HiddenModelField, self).clean(value)
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