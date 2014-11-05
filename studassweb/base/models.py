from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import User


class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')

    @classmethod
    def instance(cls):
        obj, created = cls.objects.get_or_create()
        return obj


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
    text = models.TextField(max_length=400)
    created = models.DateTimeField('Date created')
    author = models.ForeignKey(User)
