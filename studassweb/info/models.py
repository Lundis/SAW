from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from django.core.urlresolvers import reverse


class InfoCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # an info category can have an associated menu item
    menu_item = models.ForeignKey(MenuItem, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("info.views.view_category", kwargs={'category_id': self.id})


class InfoPage(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    text_html = models.TextField()
    category = models.ForeignKey(InfoCategory, null=True)

    def get_absolute_url(self):
        return reverse("info.views.view_page", kwargs={'category_id': self.category.id,
                                                       'page_id': self.id})


class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
    author = models.ForeignKey(User)
    date = models.DateTimeField('Date edited')

