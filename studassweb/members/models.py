from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    enrollment_year = models.IntegerField()
    graduated_year = models.IntegerField(default=0) # 0 if not graduated?
    # is the user a confirmed member of the association?
    confirmed = models.BooleanField(default=False)

class Payment(models.Model):
    user = models.ForeignKey(User)
    purpose = models.CharField(max_length=200)