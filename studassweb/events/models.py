from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings
import django.utils.timezone as timezone
from solo.models import SingletonModel
import events.register as eregister
from users import permissions
from base.fields import ValidatedRichTextField
from frontpage.models import FrontPageItem
import itertools
from django.core import exceptions
import logging

from operator import attrgetter


logger = logging.getLogger(__name__)

PERMISSION_CHOICES = (
    (eregister.CAN_VIEW_AND_JOIN_PUBLIC_EVENTS, "Public event"),
    (eregister.CAN_VIEW_AND_JOIN_MEMBER_EVENTS, "Members-only event"),
    (eregister.CAN_VIEW_AND_JOIN_BOARD_MEMBER_EVENTS, "Board members-only event"),
)

# This is used when the user has been adding event items to an event after signups has been made
VALUE_DOES_NOT_EXIST = "not_set"

# This should maybe be put in base or something
# TODO if the field is a boolean, it should return False / True
# TODO if the field is a integer or float, it should return appropriate type!
class MultiInputField(models.CharField, metaclass=models.SubfieldBase):
    # In an ideal world this field would save different types of values and return the right python object
    # Sadly this seems rather impossible (at least as of Django 1.7)
    # hours_wasted_here = 3
    # Please increment counter as a warning to future programmers.

    def __init__(self, *args, **kwargs):
        super(MultiInputField, self).__init__(*args, **kwargs)


# This is an actual event, for example a Christmas party
class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    text = ValidatedRichTextField(verbose_name="Description")
    start = models.DateTimeField(verbose_name="Event ends")
    stop = models.DateTimeField(verbose_name="Event starts")
    author = models.ForeignKey(User)
    signup_start = models.DateTimeField(verbose_name="Signup starts", default=timezone.now)
    signup_deadline = models.DateTimeField(verbose_name="Deadline for signups")
    permission = models.CharField(max_length=100, choices=PERMISSION_CHOICES,
                                  default=eregister.CAN_VIEW_AND_JOIN_PUBLIC_EVENTS)
    max_participants = models.IntegerField(validators=[MinValueValidator(1)], default=50)
    use_captcha = models.BooleanField(default=False, verbose_name="Use captcha when anonymous people sign up")
    send_email_for_reserves = models.BooleanField(
        default=True,
        verbose_name="Send email when someone is moved from reserve list to attending"
        )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("events_view_event", kwargs={'slug': self.slug})

    def is_before_signup_start(self):
        return timezone.now() < self.signup_start

    def is_past_signup_deadline(self):
        return timezone.now() > self.signup_deadline

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
        self.update_frontpage_item()

    def delete(self, using=None):
        super(Event, self).delete(using)
        self.update_frontpage_item()

    @classmethod
    def current_events(cls):
        """
        Returns all events that haven't ended yet
        :return:
        """
        return cls.objects.filter(stop__gte=timezone.now())

    @classmethod
    def update_frontpage_item(cls):
        event_item, created = FrontPageItem.objects.get_or_create(identifier="events/upcoming_events")
        if created:
            event_item.location = FrontPageItem.HIDDEN
            event_item.title = "Upcoming Events"
        context = Context({'events': cls.current_events().order_by("start")})
        print(context)
        template = get_template("events/frontpage_content.html")
        event_item.content = template.render(context)
        event_item.save()

    def get_items(self):
        return ItemInEvent.objects.filter(event=self).order_by('item__id')

    def count_participants(self):
        return EventSignup.objects.filter(event=self).count()

    def user_can_view_and_join(self, user):
        print(self.permission)
        return permissions.has_user_perm(user, self.permission)

    def fancy_daterange(self):
        """
        Returns a nicer version of "startdate - enddate"
        Example: instead of 22.2.2015 - 23.2.2015 this should return something like 22-23.2.2015
        """
        if self.start.year == self.stop.year:
            if self.start.month == self.stop.month:
                return "{0} - {1}.{2}.{3}".format(self.start.day,
                                                  self.stop.day, self.stop.month, self.stop.year)
            return "{0}.{1} - {2}.{3}.{4}".format(self.start.day, self.start.month,
                                                  self.stop.day, self.stop.month, self.stop.year)

        elif self.start.day == self.stop.day and self.start.month == self.stop.month:
            return "{0}.{1}.{2} - {3}".format(self.start.day, self.start.month, self.start.year,
                                              self.stop.year)

        return "{0}.{1}.{2} - {3}.{4}.{5}".format(self.start.day, self.start.month, self.start.year,
                                                  self.stop.day, self.stop.month, self.stop.year)

    def get_summary(self):
        if len(self.text) > 300:
            summary = ValidatedRichTextField.get_summary(self.text, 300)
            return "%s<p><strong>...</strong></p>" % summary
        else:
            return self.text


# Each user which signs up creates one of these
# We need both user and name as we need to allow non-signed in users to sign up
class EventSignup(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Full name")
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    auth_code = models.CharField(max_length=32, unique=True)  # Edit and delete for anonymous users
    order_id = models.IntegerField(validators=MinValueValidator(1), default=1)

    class Meta:
        ordering = "created",

    def user_can_edit(self, user):
        if self.user == user or permissions.has_user_perm(user, eregister.CAN_CREATE_EVENTS):
            return True
        else:
            return False

    def __str__(self):
        return "{0}:{1} has registered to {2}".format(self.created, self.user, self.event)

    def save(self, *args, **kwargs):
        super(EventSignup, self).save(*args, **kwargs)
        self.fix_indices()

    def delete(self, using=None):
        super(EventSignup, self).delete(using)
        if self.event.send_email_for_reserves:
            # Notify a user on the reserve list that they're in by email
            # Can't allow delete() to throw an exception related to the email
            try:
                signups = EventSignup.objects.filter(event=self.event)
                if self.event.max_participants <= signups.count():
                    # Get the signup that just got below the participant limit
                    reserve_signup = signups[self.event.max_participants - 1]
                    reserve_signup.send_reserve_email()
            except Exception as e:
                logger.error("Sending reserve email failed (%s)", e)

            # update indices
            self.fix_indices()

    def send_reserve_email(self):
        context = Context({'event': self.event})
        template = get_template("events/emails/reserve_notify.html")
        message = template.render(context)
        title = _("Reserve notification for") + " " + self.event.title
        from_email = settings.NO_REPLY_EMAIL
        to_emails = [self.email]
        send_mail(title, message, from_email, to_emails)

    def build_email_content(self, request):
        context = Context(
            {'request': request,
             'event': self.event,
             'signup': self,
             'signup_edit_url':
                 request.build_absolute_uri(reverse("events_view_event_edit_signup_by_code",
                                                    kwargs={'event_id': self.event.id,
                                                            'auth_code': self.auth_code})),
             'signup_cancel_url':
                 request.build_absolute_uri(reverse("events_delete_event_signup_by_code",
                                                    kwargs={'auth_code': self.auth_code}))}
        )

        template = get_template("events/email.html")
        return template.render(context)

    def is_reserve(self):
        signups = EventSignup.objects.filter(event=self.event)
        for index, item in enumerate(signups):
            if item.pk == self.pk:
                return index >= self.event.max_participants
        logger.error("is_reserve couldn't find itself in the list")

    def is_first_reserve(self):
        signups = EventSignup.objects.filter(event=self.event)
        for index, item in enumerate(signups):
            if item.pk == self.pk:
                return index == self.event.max_participants
        logger.error("is_first_reserve couldn't find itself in the list")

    def fix_indices(self):
        signups = EventSignup.objects.filter(event=self.event)
        for index, item in enumerate(signups):
            if item.order_id != index + 1:
                item.order_id = index + 1
                item.save()

    def get_items(self):
        return ItemInSignup.objects.filter(signup=self).order_by('item__id')

    # This function excludes items which has been removed from the event after signup was made
    # It also adds "missing" items, which exists if item events are added to event after signup was created
    def get_items_relevant(self):
        # Only these items should be returned even if more are saved
        items_in_event = ItemInEvent.objects.filter(event=self.event)
        items_in_event_itemonly = ItemInEvent.objects.filter(event=self.event).values('item')

        items_in_signup = ItemInSignup.objects.filter(signup=self).\
            filter(item__in=items_in_event_itemonly).order_by('item__id')

        items_in_signup_items = items_in_signup.values('item')
        # Get all items which are configured for event but is not in signup
        missing_items = items_in_event.exclude(item__in=items_in_signup_items)
        result = list(items_in_signup)

        # Add missing items
        for item_in_event in missing_items:
            fake_item_in_signup = ItemInSignup()
            fake_item_in_signup.signup_id = self
            fake_item_in_signup.value = VALUE_DOES_NOT_EXIST
            fake_item_in_signup.item = item_in_event.item
            result.append(fake_item_in_signup)

        # Needs to be sorted to get in right column
        result.sort(key=attrgetter('item.id'))
        return result


class EventItem(models.Model):
    TYPE_BOOL = 'B'
    TYPE_STR = 'S'
    TYPE_TEXT = 'T'
    TYPE_INT = 'I'
    TYPE_CHOICE = 'C'
    TYPE_CHOICES = (
        (TYPE_BOOL, 'Checkbox'),
        (TYPE_STR, 'Text (one line)'),
        (TYPE_TEXT, 'Text (multiple lines)'),
        (TYPE_INT, 'Integer'),
        (TYPE_CHOICE, 'Choice'),
    )

    name = models.CharField(max_length=100)
    required = models.BooleanField(default=False, verbose_name=_("Is this field mandatory"))
    public = models.BooleanField(default=False,
                                 verbose_name=_("Is this field shown to everyone?",))
    hide_in_print_view = models.BooleanField(default=False,
                                             verbose_name=_("Is this field hidden from the print view?",))
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_INT,
                            verbose_name="Data type",
                            help_text=_("Decides what kind of data is allowed in this field. The options are:<br />" +
                                        "Checkbox: A simple checkbox (yes/no)<br />" +
                                        "Text (one line): A text field with one line <br />" +
                                        "Text (multiple lines): A larger resizeable text field that allows multiple lines<br />" +
                                        "Integer: A number<br />" +
                                        "Choice: A multiple-choices field. syntax for name: question//alternative1//alternative2//alternative3")
    )

    def __str__(self):
        return str(self.name)

    def get_name(self):
        if self.type == self.TYPE_CHOICE:
            return str(self.name.split("//")[0])
        else:
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
        return str("{0} signed up with {1}: {2}".format(self.signup.name, self.item.name, self.get_value()))
        return str("{0} signed up with {1}: {2}".format(self.signup.name, self.item.name, self.get_value()))

    def get_value(self):
        if self.value == VALUE_DOES_NOT_EXIST:
            return _("(not set)")  # This string is shown for event items without a set value
        if self.value is None:
            return None
        if self.item.type in (EventItem.TYPE_CHOICE, EventItem.TYPE_STR, EventItem.TYPE_TEXT):
            return str(self.value)
        if self.item.type == EventItem.TYPE_BOOL:
            if self.value == "True":
                return True
            elif self.value == "False":
                return False
            else:
                raise TypeError()
        if self.item.type == EventItem.TYPE_INT:
            return int(self.value)
        else:
            raise NotImplementedError()


        return str("{0} signed up with {1}: {2}".format(self.signup.name, self.item.name, self.value))


class EventSettings(SingletonModel):
    is_setup = models.BooleanField(default=False)

    @classmethod
    def instance(cls):
        instance, created = cls.objects.get_or_create()
        return instance

