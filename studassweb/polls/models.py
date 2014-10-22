from django.db import models

# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    publication = models.DateTimeField('Date published')
    expiration = models.DateTimeField('Poll closes')
    # expiration date

class Choice(models.Model):
    name = models.CharField(max_length=200)
    id_to_poll = models.ForeignKey(Poll)

class Votes(models.Model):
    choice_id = models.ForeignKey(Choice)
    #User?

