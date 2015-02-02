from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from solo.models import SingletonModel
from ckeditor.fields import RichTextField


class Message(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    from_person = models.ForeignKey(User, blank=True, null=True)
    from_email = models.EmailField()
    date_and_time = models.DateTimeField(default=datetime.now, blank=True)


class Settings(SingletonModel):
    info_text = RichTextField()
    save_to_db = models.BooleanField(default=True)
    send_email = models.BooleanField(default=True)