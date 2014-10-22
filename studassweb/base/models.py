from django.db import models
from solo.models import SingletonModel
from menu.models import Menu

class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    main_menu = models.ForeignKey(Menu, blank=True, null=True)

class disabled_module(models.Model):
    app_name = models.CharField(max_length=50)


class Comment(models.Model):
    comment_text = models.TextField(max_length=400)
    comment_created = models.DateTimeField('Date created')
    comment_by_user = models.ForeignKey(LdapLink)

class UserExtension(models.Model):
    #User?
    link_to_homepage = models.CharField(max_length=400)
    enrollment_year = models.IntegerField() #does this need a default value?
    graduated_year = models.IntegerField(default=0)# 0 if not graduated?

class LdapLink(models.Model):
    #User? have to take this from members i guess but since it was empty idk
    hostname = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
