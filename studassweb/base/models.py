from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import User
from .utils import get_all_modules
from django.db import models
from urllib.request import urlopen
import json
import datetime
from io import BytesIO
import shutil


class BootswatchTheme(models.Model):
    name = models.CharField(max_length=50)
    theme_path = models.CharField(max_length=200, default="css/bootstrap.min.css")
    preview_image = models.ImageField(upload_to="base/theme_previews")
    preview_url = models.URLField()

    @classmethod
    def create_from_json(cls, json_dict, version):
        """
        Parses the theme data from the JSON
        :param json_dict:
        :return:
        """
#        preview_image_stream = BytesIO(urlopen(json_dict['thumbnail']).read())
#        filename
#        preview_image.image.save(json_dict['name'] + "_preview")
#        bst = BootswatchTheme(name=json_dict['name'],
#                              preview_image=)


class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    association_founded = models.IntegerField(default=1900)
    # main bootstrap theme css file
    bootstrap_theme_url = models.CharField(max_length=200, default="css/themes/bootstrap.min.css")
    # optional theme modifier css file
    bootstrap_theme_mod_url = models.CharField(max_length=200, default="css/themes/bootstrap-theme.min.css")
    bootswatch_version = models.CharField(max_length=50, default=None, null=True)
    bootswatch_last_checked = models.DateTimeField(default=datetime.datetime(year=2000, month=1, day=1))

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
            updated_ago = datetime.datetime.now() - instance.bootswatch_last_checked
            # Don't check for updates more often than once every week
            if updated_ago < datetime.timedelta(week=1):
                return
        cls._update_bootswatch()

    @classmethod
    def _update_bootswatch(cls):
        data = urlopen("http://api.bootswatch.com/3/").read().decode()
        data_dict = json.loads(data)


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
