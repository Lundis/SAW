from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext as _
import json
from io import BytesIO
import shutil
import os
import datetime
import re
from concurrent import futures
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
import logging
from solo.models import SingletonModel
from .utils import get_all_modules, get_modules_with


logger = logging.getLogger(__name__)

THEME_DIR = os.path.join("css", "bootswatch_themes")


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

        # first download the image
        try:
            preview_image_stream = BytesIO(urlopen(json_dict['thumbnail']).read())
        except HTTPError:
            logger.error("Failed to fetch theme %s" % json_dict['name'])
            return
        original_image_filename = urlparse(json_dict['thumbnail']).path.split("/")[-1]

        image_folder = os.path.join("base",
                                    "bootswatch",
                                    version)
        image_absolute_folder = os.path.join(settings.MEDIA_ROOT, image_folder)
        if not os.path.exists(image_absolute_folder):
            os.makedirs(image_absolute_folder)
        image_filename = json_dict['name'] + "_" + original_image_filename
        image_absolute_path = os.path.join(image_absolute_folder, image_filename)
        image_relative_path = os.path.join(image_folder, image_filename)
        # save the image to disk - overwrite old file (it shouldn't exist)
        with open(image_absolute_path, 'wb') as out_file:
            logger.info("Saving preview image: %s", image_absolute_path)
            shutil.copyfileobj(preview_image_stream, out_file)

        # same for the css file
        try:
            theme_stream = BytesIO(urlopen(json_dict['cssMin']).read())
        except HTTPError:
            logger.error("Failed to fetch theme %s" % json_dict['name'])
            return
        theme_filename = urlparse(json_dict['cssMin']).path.split("/")[-1]
        theme_folder = os.path.join(THEME_DIR, version, json_dict['name'])
        theme_absolute_folder = os.path.join(settings.STATIC_DIR, theme_folder)
        if not os.path.exists(theme_absolute_folder):
            os.makedirs(theme_absolute_folder)
        theme_absolute_path = os.path.join(theme_absolute_folder, theme_filename)
        theme_relative_path = os.path.join(theme_folder, theme_filename)
        with open(theme_absolute_path, 'wb') as out_file:
            logger.info("Saving theme css: %s", theme_absolute_path)
            shutil.copyfileobj(theme_stream, out_file)

        try:
            # update old entry if it exists
            bst = cls.objects.get(name=json_dict['name'])
            bst.theme_path = theme_relative_path
            bst.preview_image = image_relative_path
            bst.preview_url = json_dict['preview']
        except cls.DoesNotExist:
            # otherwise create a new one
            bst = BootswatchTheme(name=json_dict['name'],
                                  theme_path=theme_relative_path,
                                  preview_image=image_relative_path,
                                  preview_url=json_dict['preview'])

        return bst.save()


THEME_DEFAULT_CSS = "css/themes/bootstrap.min.css"
THEME_DEFAULT_CSS_MOD = "css/themes/bootstrap-theme.min.css"


class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    base_url = models.CharField(max_length=150, default='http://localhost:8000')
    association_contact_email = models.EmailField(max_length=254, default='example@example.com')
    association_founded = models.IntegerField(default=1900)
    # main bootstrap theme css file
    bootstrap_theme_url = models.CharField(max_length=200, default=THEME_DEFAULT_CSS)
    # optional theme modifier css file
    bootstrap_theme_mod_url = models.CharField(max_length=200, null=True, blank=True, default=THEME_DEFAULT_CSS_MOD)
    bootswatch_version = models.CharField(max_length=50, default=None, null=True)
    bootswatch_last_checked = models.DateTimeField(default=timezone.datetime(year=2000, month=1, day=1))

    show_feedback_helptext = models.BooleanField(default=True)

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
        try:
            data = urlopen("http://api.bootswatch.com/3/").read().decode()
        except HTTPError:
            logger.error("Failed to fetch bootswatch theme descriptor %s")
            return
        data_dict = json.loads(data)
        version = data_dict['version']
        with futures.ThreadPoolExecutor(max_workers=16) as executor:
            for theme_data in data_dict['themes']:
                #BootswatchTheme.create_from_json(theme_data, version)
                executor.submit(BootswatchTheme.create_from_json, theme_data, version)

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

    @classmethod
    def execute_for_all_enabled(cls, module, func_name):
        """
        execute the specified function from the specified module in all enabled apps where it exists
        :return:
        """
        mod_funcs = get_modules_with(module, func_name)

        for mod, func in mod_funcs:
            if cls.is_enabled(mod):
                func()


class Comment(models.Model):
    text = models.TextField(max_length=400)
    created = models.DateTimeField('Date created', auto_now_add=True)
    author = models.ForeignKey(User)

    # A generic field for linking to any model
    _content_type = models.ForeignKey(ContentType)
    _object_id = models.PositiveIntegerField()
    target = GenericForeignKey('_content_type', '_object_id')

    class Meta:
        ordering = ("_object_id", "created")

    def set_target(self, target):
        """
        :param target: A Django Model
        :return:
        """
        self._content_type = ContentType.objects.get_for_model(target)
        self._object_id = target.id

    @classmethod
    def get_comments_for_object(cls, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return cls.objects.filter(_content_type=content_type, _object_id=obj.id)

    def __str__(self):
        return "%s#%s" % (self.target, self.id)


class Feedback(models.Model):
    FEEDBACK_HELPTEXT = "HELPTEXT"
    FEEDBACK_CHOICES = (
        (FEEDBACK_HELPTEXT, "Help text feedback"),
    )
    RESPONSE_GOOD = "GOOD"
    RESPONSE_BAD = "BAD"
    RESPONSE_UNNECESSARY = "UNNE"
    RESPONSE_CHOICES = (
        (RESPONSE_GOOD, "Good"),
        (RESPONSE_BAD, "Bad"),
        (RESPONSE_UNNECESSARY, "Unnecessary"),
    )

    user = models.ForeignKey(User, blank=True, null=True)
    url = models.CharField(max_length=300)
    ip_address = models.IPAddressField()
    type = models.CharField(max_length=10, choices=FEEDBACK_CHOICES)
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("type", "user", "url", "ip_address"),
            ("type", "user", "url")
        )

    @classmethod
    def can_user_give_feedback(cls, user, ip, type, url):
        url = cls.strip_url(url)
        if user.is_authenticated():
            object = cls.objects.filter(type=type, user=user, url=url)
            logger.debug("type: %s, user: %s, url: %s" % (type, user, url))
            logger.debug(object)
            return not object.exists()
        else:
            return not cls.objects.filter(type=type, ip_address=ip, url=url).exists()

    @classmethod
    def strip_url(cls, url):
        """
        Strip away stuff like page IDs. Does nothing for slugs.
        :param url:
        :return:
        """
        p = re.compile(r"(/\d+/)")
        url = p.sub("/<id?>/", url)
        # also remove any weird characters for security purposes
        whitelist = re.compile(r"([^a-zA-Z0-9\-_<>/])")
        url = whitelist.sub("", url)
        return url

    def clean(self):
        """
        Clean the URL
        :return:
        """
        self.url = self.strip_url(self.url)