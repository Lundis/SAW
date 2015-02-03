from django.template import Library
from contact.models import Settings
register = Library()


@register.assignment_tag
def is_writing_messages_enabled():
    return Settings.get_solo().save_to_db or Settings.get_solo().send_email

@register.assignment_tag
def is_message_to_db_enabled():
    return Settings.get_solo().save_to_db