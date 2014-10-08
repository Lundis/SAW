from django.db import models

class Menu(models.Model):
    menu_name = models.CharField(max_length=30, unique=True)
    template = models.CharField(max_length=100)

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)
    app_name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    display_order = models.IntegerField()
    visible = models.BooleanField(default=True)
    url = models.CharField(max_length=100)
    auto_created = models.BooleanField(default=False)
