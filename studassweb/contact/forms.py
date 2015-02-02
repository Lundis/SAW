from django import forms
from .models import Message, Settings


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('from_email', 'title', 'message', )

class SettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ('info_text', 'save_to_db', 'send_email', )