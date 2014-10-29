from django.db import models
from solo.models import SingletonModel
from menu.models import Menu
from django.contrib.auth.models import User

class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    main_menu = models.ForeignKey(Menu, blank=True, null=True)

    @classmethod
    def instance(cls):
        return cls.objects.get()


class DisabledModule(models.Model):
    app_name = models.CharField(max_length=50, unique=True)

    @classmethod
    def is_disabled(cls, name):
        return cls.objects.filter(app_name=name).count() == 1

    @classmethod
    def is_enabled(cls, name):
        return not cls.is_disabled(name)

    @classmethod
    def disable(cls, name):
        try:
            mod = cls.objects.get(app_name=name)
            # if it exists do nothing
        except cls.DoesNotExist:
            # if it doesn't, add it
            mod = DisabledModule(app_name=name)
            mod.save()

    @classmethod
    def enable(cls, name):
        try:
            mod = cls.objects.get(app_name=name)
            mod.delete()
        except cls.DoesNotExist:
            # Nothing to be done
            pass


class Comment(models.Model):
    comment_text = models.TextField(max_length=400)
    comment_created = models.DateTimeField('Date created')
    comment_by_user = models.ForeignKey(LdapLink)

class UserExtension(models.Model):
    user = models.ForeignKey(User)
    link_to_homepage = models.CharField(max_length=400)
    enrollment_year = models.IntegerField() #does this need a default value?
    graduated_year = models.IntegerField(default=0)# 0 if not graduated?

class LdapLink(models.Model):
    user = models.ForeignKey(User)
    hostname = models.CharField(max_length=200)
    username = models.CharField(max_length=50)

