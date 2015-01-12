from django.db import models
from django.core.validators import ValidationError
from django.utils.translation import ugettext as _
from users.groups import put_user_in_default_group, MEMBER
from users.models import UserExtension
from base.models import SiteConfiguration


class Member(models.Model):
    user_ext = models.ForeignKey(UserExtension, null=True, blank=True, unique=True, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    enrollment_year = models.IntegerField(null=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    # is the user a confirmed member of the association?
    confirmed = models.BooleanField(default=False)
    # is the user applying for membership?
    applying = models.BooleanField(default=False)
    # can the user apply for membership?
    can_apply_for_membership = models.BooleanField(default=True)

    def confirm(self):
        self.confirmed = True
        self.applying = False
        self.save()
        # give additional rights to user if he doesn't already have them.
        if not self.user_ext.user.groups.filter(name=MEMBER).exists():
            put_user_in_default_group(self.user_ext.user, MEMBER)

    def deny(self):
        self.confirmed = False
        self.applying = False
        self.save()

    def deny_permanently(self):
        self.deny()
        self.can_apply_for_membership = False
        self.save()

    def __str__(self):
        return "{} {}[{}->{}]".format(self.first_name,
                                      self.last_name,
                                      str(self.enrollment_year),
                                      str(self.graduation_year))

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


class PaymentPurpose(models.Model):
    purpose = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Payment(models.Model):
    member = models.ForeignKey(Member)
    purpose = models.ForeignKey(PaymentPurpose)


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