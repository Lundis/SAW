from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from .register import CAN_CREATE_EVENTS
from users import permissions


# This should maybe be put in base or something
class MultiInputField(models.CharField):
    description = "This is magic"

    def __init__(self, *args, **kwargs):
        super(MultiInputField, self).__init__(*args, **kwargs)
        #self.validators.append(validators.MaxLengthValidator(self.max_length))


#This is an actual event, for example a Christmas party
# TODO is it public, for members, or for board members only?
# TODO slug for urls
class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=500)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    author = models.ForeignKey(User)
    signup_deadline = models.DateTimeField()
    permission = models.CharField(max_length=100, blank=True, null=True)  # Permission needed to see and attend

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("events_view_event", kwargs={'event_id': self.id})


#Each user which signs up creates one of these
#We need both user and name as we need to allow non-signed in users to sign up
# TODO we need to save the auth_codes somehow, to ensure that a new signup doesn't get the same code as a delete one
class EventSignup(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    matricle = models.CharField(max_length=20)
    association = models.CharField(max_length=200)
    diet = models.CharField(max_length=200, null=True, blank=True)
    other = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    auth_code = models.CharField(max_length=32, unique=True)  # Edit and delete for anonymous users

    def user_can_edit(self, user):
        print(self.name)
        print(self.user)
        print(user)
        if self.user == user or permissions.has_user_perm(user, CAN_CREATE_EVENTS):
            return True
        else:
            return False


class EventItem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


# This is for setting which items can be set when signing up to event
class ItemInEvent(models.Model):
    TYPE_BOOL = 'B'
    TYPE_STR = 'S'
    TYPE_INT = 'I'
    TYPE_CHOICE = 'C'
    TYPE_CHOICES = (
        (TYPE_BOOL, 'Boolean'),
        (TYPE_STR, 'String'),
        (TYPE_INT, 'Integer'),
        (TYPE_CHOICE, 'Choice'),
    )

    event = models.ForeignKey(Event)
    item = models.ForeignKey(EventItem)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_INT)

    def __str__(self):
        return str("{0} is enabled in {1}".format(self.item.name, self.event.title))


# This is for one specific signup
class ItemInSignup(models.Model):
    signup = models.ForeignKey(EventSignup)
    item = models.ForeignKey(EventItem)
    amount = models.IntegerField()
    value = MultiInputField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str("{0} signed up for {1} {2}".format(self.signup.name, self.amount, self.item.name))


