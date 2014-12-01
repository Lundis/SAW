from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    enrollment_year = models.IntegerField()
    graduation_year = models.IntegerField(null=True)
    # is the user a confirmed member of the association?
    confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(User)


class PaymentPurpose(models.Model):
    purpose = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Payment(models.Model):
    user = models.ForeignKey(User)
    purpose = models.ForeignKey(PaymentPurpose)