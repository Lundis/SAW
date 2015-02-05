from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField
from solo.models import SingletonModel


class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    info_text = RichTextField()
    save_to_db = models.BooleanField(default=True)
    send_email = models.BooleanField(default=True)
    email = models.EmailField()
    ordering_index = models.IntegerField(unique=True)

    class Meta:
        ordering = "ordering_index",

    @classmethod
    def _get_by_index(cls, index):
        try:
            return cls.objects.get(ordering_index=index)
        except cls.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        old_with_index = self._get_by_index(self.ordering_index)
        if old_with_index and old_with_index.id != self.id:
            old_with_index.ordering_index += 1
            old_with_index.save()
        super(ContactInfo, self).save(*args, **kwargs)


class Message(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    from_person = models.ForeignKey(User, blank=True, null=True)
    from_email = models.EmailField()
    date_and_time = models.DateTimeField(default=datetime.now, blank=True)
    contact = models.ForeignKey(ContactInfo)


class ContactSettings(SingletonModel):
    _is_setup = models.BooleanField(default=False)

    @classmethod
    def is_setup(cls):
        return cls.objects.get_or_create()[0]._is_setup
