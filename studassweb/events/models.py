from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    author = models.ForeignKey(User)
    signup_deadline = models.DateTimeField()

class EventSignup(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    matricle = models.CharField(max_length=20)
    association = models.CharField(max_length=200)
    diet = models.CharField(max_length=200)
    other = models.CharField(max_length=200)

class EventItem(models.Model):
    name = models.CharField(max_length=100)

class ItemInEvent(models.Model):
    event = models.ForeignKey(Event)
    item = models.ForeignKey(EventItem)

class ItemInSignup(models.Model):
    signup = models.ForeignKey(EventSignup)
    item = models.ForeignKey(EventItem)
    amount = models.IntegerField()
