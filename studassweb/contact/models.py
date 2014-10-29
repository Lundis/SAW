from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ContactForm(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    from_person = models.ForeignKey(User)
    from_email = models.EmailField()
    date_and_time = models.DateTimeField()

