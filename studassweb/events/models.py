from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from .register import CAN_CREATE_EVENTS
from users import permissions
from django.template.defaultfilters import slugify
import itertools


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

    # https://keyerror.com/blog/automatically-generating-unique-slugs-in-django
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug and ensure it is unique

            max_length = Event._meta.get_field('slug').max_length
            temp_slug = orig = slugify(self.title)[:max_length]
            for x in itertools.count(1):
                if not Event.objects.filter(slug=temp_slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                temp_slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

            self.slug = temp_slug
        super(Event, self).save(*args, **kwargs)



#Each user which signs up creates one of these
#We need both user and name as we need to allow non-signed in users to sign up
# TODO we need to save the auth_codes somehow, to ensure that a new signup doesn't get the same code as a delete one
class EventSignup(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField(default=datetime.now, blank=True)
    auth_code = models.CharField(max_length=32, unique=True)  # Edit and delete for anonymous users

    def user_can_edit(self, user):
        if self.user == user or permissions.has_user_perm(user, CAN_CREATE_EVENTS):
            return True
        else:
            return False

    def __str__(self):
        return "{0}:{1} has registered to {2}".format(self.created, self.user, self.event)


class EventItem(models.Model):
    TYPE_BOOL = 'B'
    TYPE_STR = 'S'
    TYPE_TEXT = 'T'
    TYPE_INT = 'I'
    TYPE_CHOICE = 'C'
    TYPE_CHOICES = (
        (TYPE_BOOL, 'Boolean'),
        (TYPE_STR, 'String'),
        (TYPE_TEXT, 'Text'),
        (TYPE_INT, 'Integer'),
        (TYPE_CHOICE, 'Choice'),
    )

    name = models.CharField(max_length=100)
    required = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_INT)

    def __str__(self):
        return str(self.name)


# This is for setting which items can be set when signing up to event
class ItemInEvent(models.Model):
    event = models.ForeignKey(Event)
    item = models.ForeignKey(EventItem)

    def __str__(self):
        return str("{0} is enabled in {1}".format(self.item.name, self.event.title))


# This is for one specific signup
class ItemInSignup(models.Model):
    signup = models.ForeignKey(EventSignup)
    item = models.ForeignKey(EventItem)
    value = MultiInputField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str("{0} signed up with {1}: {2}".format(self.signup.name, self.item.name, self.value))


