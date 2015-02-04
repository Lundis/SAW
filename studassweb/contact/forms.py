from django import forms
from .models import Message, ContactInfo


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('from_email', 'title', 'message', )

    def save(self, commit=True, contact=None, from_person=None):
        """
        Note: You MUST specifiy the contact
        :param commit:
        :param contact:
        :return:
        """
        obj = super(MessageForm, self).save(commit=False)
        obj.contact = contact
        if from_person and from_person.is_authenticated():
            obj.from_person = from_person
        super(MessageForm, self).save(commit=commit)


class ContactSettingsForm(forms.ModelForm):

    class Meta:
        model = ContactInfo
        fields = ('name', 'info_text', 'save_to_db', 'send_email', 'email', "ordering_index")
