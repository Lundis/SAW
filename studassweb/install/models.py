# coding=utf-8
from django.db import models

from solo.models import SingletonModel


class InstallProgress(SingletonModel):
    """
    Keeps track of the installation progress
    """
    installed = models.BooleanField(default=False)

    site_name_ok = models.BooleanField(default=False)
    modules_ok = models.BooleanField(default=False)
    menu_ok = models.BooleanField(default=False)

    @classmethod
    def site_name_set(cls):
        """
        Marks the site name as set
        :return:
        """
        progress, created = cls.objects.get_or_create()
        progress.site_name_ok = True
        progress.save()

    @classmethod
    def is_site_name_set(cls):
        progress, created = cls.objects.get_or_create()
        return progress.site_name_ok

    @classmethod
    def modules_set(cls):
        """
        Marks the modules as selected
        :return:
        """
        progress, created = cls.objects.get_or_create()
        progress.modules_ok = True
        progress.save()

    @classmethod
    def is_modules_set(cls):
        progress, created = cls.objects.get_or_create()
        return progress.modules_ok

    @classmethod
    def menu_set(cls):
        """
        Marks the menu as set up
        :return:
        """
        progress, created = cls.objects.get_or_create()
        progress.menu_ok = True
        progress.save()

    @classmethod
    def is_menu_set(cls):
        progress, created = cls.objects.get_or_create()
        return progress.menu_ok

    @classmethod
    def finish(cls):
        """
        Checks that all parts of the installation are completed, then marks it as installed
        """
        progress, created = cls.objects.get_or_create()
        if progress.site_name_ok and progress.modules_ok and progress.menu_ok:
            progress.installed = True
        else:
            progress.installed = False
        progress.save()

    @classmethod
    def is_finished(cls):
        """
        :return: A boolean indicating whether the installation is finished or not.
        """
        progress, created = cls.objects.get_or_create()
        return progress.installed
