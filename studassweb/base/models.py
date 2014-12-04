from solo.models import SingletonModel
from django.contrib.auth.models import User
from django.db import models
from urllib.request import urlopen
from urllib.parse import urlparse
from django.conf import settings
from django.utils import timezone
import json
from io import BytesIO
import shutil
import os
import datetime
from concurrent import futures
from .utils import get_all_modules

THEME_DIR = os.path.join(settings.STATIC_DIR, "css", "themes")


class BootswatchTheme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    theme_path = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to="base/bootswatch")
    preview_url = models.URLField()

    def __str__(self):
        return self.name

    @classmethod
    def create_from_json(cls, json_dict, version):
        """
        Parses the theme data from the JSON
        :param json_dict:
        :return:
        """
        # http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

        #first download the image
        preview_image_stream = BytesIO(urlopen(json_dict['thumbnail']).read())
        original_image_filename = urlparse(json_dict['thumbnail']).path.split("/")[-1]
        image_folder = os.path.join(settings.MEDIA_ROOT, "base", "bootswatch", version)
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        image_filename = json_dict['name'] + "_" + original_image_filename
        image_path = os.path.join(image_folder, image_filename)
        # save the image to disk - overwrite old file (it shouldn't exist)
        with open(image_path, 'wb') as out_file:
            shutil.copyfileobj(preview_image_stream, out_file)

        # same for the css file
        theme_stream = BytesIO(urlopen(json_dict['cssMin']).read())
        theme_filename = urlparse(json_dict['cssMin']).path.split("/")[-1]
        theme_folder = os.path.join(THEME_DIR, version, json_dict['name'])
        if not os.path.exists(theme_folder):
            os.makedirs(theme_folder)
        theme_path = os.path.join(theme_folder, theme_filename)
        with open(theme_path, 'wb') as out_file:
            shutil.copyfileobj(theme_stream, out_file)

        try:
            # update old entry if it exists
            bst = cls.objects.get(name=json_dict['name'])
            bst.theme_path = theme_path
            bst.preview_image = image_filename
            bst.preview_url = json_dict['preview']
        except cls.DoesNotExist:
            # otherwise create a new one
            bst = BootswatchTheme(name=json_dict['name'],
                                  theme_path=theme_path,
                                  preview_image=image_filename,
                                  preview_url=json_dict['preview'])

        return bst.save()


class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    association_founded = models.IntegerField(default=1900)
    # main bootstrap theme css file
    bootstrap_theme_url = models.CharField(max_length=200, default="css/themes/bootstrap.min.css")
    # optional theme modifier css file
    bootstrap_theme_mod_url = models.CharField(max_length=200, default="css/themes/bootstrap-theme.min.css")
    bootswatch_version = models.CharField(max_length=50, default=None, null=True)
    bootswatch_last_checked = models.DateTimeField(default=timezone.datetime(year=2000, month=1, day=1))

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

    @classmethod
    def update_bootswatch(cls):
        """
        Updates bootswatch if it's outdated
        :return:
        """
        instance = cls.instance()
        if instance.bootswatch_version:
            updated_ago = timezone.now() - instance.bootswatch_last_checked
            # Don't check for updates more often than once a week
            if updated_ago < datetime.timedelta(weeks=1):
                return
        cls._update_bootswatch()

    @classmethod
    def _update_bootswatch(cls):
        data = urlopen("http://api.bootswatch.com/3/").read().decode()
        data_dict = json.loads(data)
        version = data_dict['version']
        with futures.ThreadPoolExecutor(max_workers=16) as executor:
            for theme_data in data_dict['themes']:
                #BootswatchTheme.create_from_json(theme_data, version)
                future = executor.submit(BootswatchTheme.create_from_json, theme_data, version)
            print(future.result())

        instance = cls.instance()
        instance.bootswatch_version = version
        instance.bootswatch_last_checked = timezone.datetime.now()
        instance.save()


class DisabledModule(models.Model):
    app_name = models.CharField(max_length=50, unique=True)

    @classmethod
    def is_disabled(cls, name):
        return cls.objects.filter(app_name=name).exists()

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
