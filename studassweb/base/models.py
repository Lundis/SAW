from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import User
from .utils import get_all_modules


class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    association_founded = models.IntegerField(default=1900)
    bootstrap_theme_url = models.CharField(max_length=200, default="css/bootstrap.min.css")

    @classmethod
    def instance(cls):
        obj, created = cls.objects.get_or_create()
        return obj

    @classmethod
    def founded(cls):
        """

        :return: The year this association was founded
        """
        return cls.instance().association_founded


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

    @classmethod
    def get_all_enabled_modules(cls):
        all_modules = get_all_modules()
        return [mod for mod in all_modules if cls.is_enabled(mod)]


class Comment(models.Model):
    text = models.TextField(max_length=400)
    created = models.DateTimeField('Date created')
    author = models.ForeignKey(User)
