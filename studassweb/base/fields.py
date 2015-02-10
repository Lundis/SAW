from ckeditor.fields import RichTextField, RichTextFormField
from .html_tag_closer import complete_html


class ValidatedRichTextField(RichTextField):
    """
    This class changes the default form field, to use a custom one that automatically closes HTML tags.
    """

    def formfield(self, **kwargs):
        # Change the default form field
        if not 'form_class' in kwargs:
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