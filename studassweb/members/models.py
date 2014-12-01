from django.db import models
from django.contrib.auth.models import User
from users.groups import put_user_in_default_group, MEMBER
import users.models


class Member(models.Model):
    enrollment_year = models.IntegerField()
    graduation_year = models.IntegerField(null=True)
    # is the user a confirmed member of the association?
    confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def confirm(self):
        self.confirmed = True
        self.save()
        # give additional rights to user if he doesn't already have them.
        if not self.user.groups.filter(name=MEMBER).exists():
            put_user_in_default_group(self.user, MEMBER)

    def deny(self):
        self.delete()

    def deny_permanently(self):
        user_ext = users.models.UserExtension.objects.get(user=self.user)
        user_ext.can_apply_for_membership = False
        user_ext.save()

    def __str__(self):
        return "{} {}[{}->{}]".format(self.user.first_name,
                                      self.user.last_name,
                                      str(self.enrollment_year),
                                      str(self.graduation_year))


class PaymentPurpose(models.Model):
    purpose = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Payment(models.Model):
    user = models.ForeignKey(User)
    purpose = models.ForeignKey(PaymentPurpose)