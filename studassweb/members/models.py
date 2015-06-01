from django.db import models
from django.core.validators import ValidationError, MinValueValidator
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User
from users.groups import put_user_in_standard_group, MEMBER
from users.models import UserExtension
from base.models import SiteConfiguration
from django.utils import timezone


class Member(models.Model):
    user_ext = models.OneToOneField(UserExtension, null=True, blank=True, unique=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    enrollment_year = models.IntegerField(null=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    # is the user a confirmed member of the association?
    confirmed = models.BooleanField(default=False)
    # is the user applying for membership?
    applying = models.BooleanField(default=False)
    # can the user apply for membership?
    can_apply_for_membership = models.BooleanField(default=True)

    class Meta:
        unique_together = ("first_name", "last_name", "email")

    def confirm(self):
        self.confirmed = True
        self.applying = False
        self.save()
        # Give additional rights to user if he doesn't already have them.
        if not self.user_ext.user.groups.filter(name=MEMBER).exists():
            put_user_in_standard_group(self.user_ext.user, MEMBER)

    def deny(self):
        self.confirmed = False
        self.applying = False
        self.save()

    def deny_permanently(self):
        self.deny()
        self.can_apply_for_membership = False
        self.save()
    
    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        s = self.get_full_name()
        if self.user_ext:
            s += " (%s)" % self.user_ext.user.username
        return s

    def clean(self):
        super(Member, self).clean()
        if self.enrollment_year is not None:
            if self.enrollment_year < SiteConfiguration.founded():
                raise ValidationError(_("Enrollment year cannot be before the association was founded"))
            if self.graduation_year is not None:
                if self.enrollment_year > self.graduation_year:
                    raise ValidationError(_("Graduation year cannot be before enrollment year"))

    @classmethod
    def create_from_user_ext(cls, user_ext, confirmed=False):
        return cls.objects.create(user_ext=user_ext,
                                  first_name=user_ext.user.first_name,
                                  last_name=user_ext.user.last_name,
                                  email=user_ext.user.email,
                                  confirmed=confirmed)


@receiver(post_delete, sender=Member, dispatch_uid="member_post_delete")
def member_post_delete(**kwargs):
    instance = kwargs.pop("instance")
    # Remove the UserExtension if it exists
    if instance.user_ext:
        instance.user_ext.delete()


@receiver(post_save, sender=Member, dispatch_uid="member_post_save")
def member_post_save(**kwargs):
    instance = kwargs.pop("instance")
    # Update first/last name of user if there's a mismatch
    if instance.user_ext:
        user = instance.user_ext.user
        if user.first_name != instance.first_name or user.last_name != instance.last_name:
            user.first_name = instance.first_name
            user.last_name = instance.last_name


class PaymentPurpose(models.Model):
    purpose = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.purpose


class Payment(models.Model):
    member = models.ForeignKey(Member)
    purpose = models.ForeignKey(PaymentPurpose)
    date = models.DateField()
    expires = models.DateField()
    date_entered = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User)

    class Meta:
        ordering = ("-expires",)

    def has_expired(self):
        return timezone.now() > self.expires

    @classmethod
    def get_latest(cls, purpose, member):
        return cls.objects.filter(purpose=purpose, member=member).first()


class CustomField(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)


class CustomEntry(models.Model):
    field = models.ForeignKey(CustomField)
    member = models.ForeignKey(Member)
    content = models.TextField(default="")

    class Meta:
        unique_together = ("field", "member")

    def __str__(self):
        return self.field.name + " for " + str(self.member)