from django import forms
from django.core.validators import ValidationError
from django.utils.translation import ugettext as _
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


class MarkAsHandledForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        Takes a message when creating it
        :param args:
        :param kwargs:
        :return:
        """
        if 'message' in kwargs:
            message = kwargs.pop('message')
        else:
            message = None
        super(MarkAsHandledForm, self).__init__(*args, **kwargs)
        if message is not None:
            if message.handled:
                raise ValueError("message %s has already been handled", message)
            self.fields['message_id'] = forms.IntegerField(initial=message.id,
                                                           widget=forms.HiddenInput())

    def clean(self):
        super(MarkAsHandledForm, self).clean()
        try:
            msg = Message.objects.get(id=self.cleaned_data['message_id'])
            if msg.handled:
                raise ValidationError(_("The specified message has already been marked as handled!"))
        except Message.DoesNotExist:
            raise ValidationError(_("The specified message does not exist"))

    def save(self):
        if self.is_valid():
            msg = Message.objects.get(id=self.cleaned_data['message_id'])
            msg.handled = True
            msg.save()