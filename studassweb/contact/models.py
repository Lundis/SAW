from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime
from base.fields import ValidatedRichTextField
from solo.models import SingletonModel


class ContactInfo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    info_text = ValidatedRichTextField(verbose_name=_("Contact details text"))
    save_to_db = models.BooleanField(default=True, verbose_name=_("Should the message be saved to the database?"))
    send_email = models.BooleanField(default=True, verbose_name=_("Should the message be sent to the specified email?"))
    email = models.EmailField()
    ordering_index = models.IntegerField(verbose_name=_("The position of this contact in the list of contacts"),
                                         validators=[MinValueValidator(1)])

    class Meta:
        ordering = "ordering_index",

    @classmethod
    def _get_by_index(cls, index):
        try:
            return cls.objects.get(ordering_index=index)
        except cls.DoesNotExist:
            return None

    def has_recipients(self):
        return self.save_to_db or self.send_email

    def save(self, *args, **kwargs):
        old_with_index = self._get_by_index(self.ordering_index)
        if old_with_index and old_with_index.id != self.id:
            old_with_index.ordering_index += 1
            old_with_index.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def messages(self):
        return Message.objects.filter(contact=self)

    def unread_messages(self):
        return self.messages().filter(handled=False)


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Subject"))
    message = models.TextField(max_length=500, verbose_name=_("Message"))
    from_person = models.ForeignKey(User, blank=True, null=True)
    from_email = models.EmailField(verbose_name=_("Your email"))
    date_and_time = models.DateTimeField(default=datetime.now, blank=True)
    contact = models.ForeignKey(ContactInfo)
    handled = models.BooleanField(default=False,
                                  blank=True,
                                  verbose_name=_("Has this message been handled by someone?"))

    class Meta:
        ordering = "-date_and_time",

    def __str__(self):
        return self.title


class ContactSettings(SingletonModel):
    _is_setup = models.BooleanField(default=False, help_text=_("Tells us if the first-time setup has been done"))

    @classmethod
    def is_setup(cls):
        return cls.objects.get_or_create()[0]._is_setup
