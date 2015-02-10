from django import forms
from captcha.fields import ReCaptchaField
from .models import Message, ContactInfo
import logging

logger = logging.getLogger(__name__)


class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            user = kwargs.pop('user')
        else:
            user = None
        super(MessageForm, self).__init__(*args, **kwargs)
        if user is not None and user.is_authenticated():
            logger.debug("MessageForm user: \"%s\"" % user)
            logger.debug("MessageForm user email: \"%s\"" % user.email)
            self.fields["from_email"].initial = user.email
        else:
            self.fields['captcha'] = ReCaptchaField()

    class Meta:
        model = Message
        fields = ('from_email', 'title', 'message', )

    def save(self, commit=True, contact=None, from_person=None):
        """
        Note: You MUST specify the contact
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
