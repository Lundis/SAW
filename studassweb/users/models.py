from django.db import models
from django.contrib.auth.models import User

class UserExtension(models.Model):
    user = models.ForeignKey(User)
    # A field where the user can write a short introduction to themselves
    description = models.TextField(max_length=1000)
    link_to_homepage = models.CharField(max_length=400)


class LdapLink(models.Model):
    user = models.ForeignKey(User)
    hostname = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
