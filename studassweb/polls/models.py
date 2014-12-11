from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    publication = models.DateTimeField('Date published')
    expiration = models.DateTimeField('Poll closes')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("polls.views.view_polls", kwargs={'poll_id': self.id})
    # expiration date

class Choice(models.Model):
    name = models.CharField(max_length=200)
    id_to_poll = models.ForeignKey(Poll)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("polls.views.set_user_choice", kwargs={'choice_id': self.id})

class Votes(models.Model):
    choice_id = models.ForeignKey(Choice)
    members_choice = models.ForeignKey(User)

