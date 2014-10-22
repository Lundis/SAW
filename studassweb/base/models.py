from django.db import models
from solo.models import SingletonModel
from menu.models import Menu

class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
    main_menu = models.ForeignKey(Menu, blank=True, null=True)

class disabled_module(models.Model):
    app_name = models.CharField(max_length=50)