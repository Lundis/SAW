from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


#This is an actual event, for example a Christmas party
class Event(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    author = models.ForeignKey(User)
    signup_deadline = models.DateTimeField()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("events_view_event", kwargs={'event_id': self.id})


#Each user which signs up creates one of these
#We need both user and name as we need to allow non-signed in users to sign up
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


#Things you can choose in event? examples?
class ItemInEvent(models.Model):
    event = models.ForeignKey(Event)
    item = models.ForeignKey(EventItem)


#Things you can choose in signup? examples?
class ItemInSignup(models.Model):
    signup = models.ForeignKey(EventSignup)
    item = models.ForeignKey(EventItem)
    amount = models.IntegerField()
