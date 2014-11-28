from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from menu.models import MenuItem, Menu
from users.groups import GUEST, MEMBER, BOARD_MEMBER
from .register import VIEW_BOARD, VIEW_MEMBER, VIEW_PUBLIC

PERMISSION_CHOICES = (
    (GUEST, VIEW_PUBLIC),
    (MEMBER, VIEW_MEMBER),
    (BOARD_MEMBER, VIEW_BOARD),
)


class InfoCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # an info category has an associated menu item, which in turn has a submenu
    menu_item = models.ForeignKey(MenuItem, null=True)

    permission = models.CharField(max_length=100, choices=PERMISSION_CHOICES, default=GUEST)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("info.views.view_category", kwargs={'category_id': self.id})

    def pages(self):
        return InfoPage.objects.filter(category=self)

    def save(self, *args, **kwargs):
        super(InfoCategory, self).save(*args, **kwargs)
        # create a menu item if it doesn't exist
        self.menu_item, created = MenuItem.get_or_create(__package__,
                                                         self.name,
                                                         linked_object=self,
                                                         permission=self.permission)
        if created:
            self.menu_item.submenu, created2 = Menu.get_or_create(__package__ + "_category_" + self.name)
            self.menu_item.save()
            self.save()

    def delete(self, *args, **kwargs):
        MenuItem.delete_all_that_links_to(self)
        super(InfoCategory, self, *args, **kwargs)


class InfoPage(models.Model):
    title = models.CharField(max_length=50)
    text = RichTextField()
    category = models.ForeignKey(InfoCategory, null=True)
    permission = models.CharField(max_length=100, choices=PERMISSION_CHOICES, default=GUEST)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("info.views.view_page", kwargs={'page_id': self.id})

    def save(self, *args, **kwargs):
        super(InfoPage, self).save(*args, **kwargs)
        # create a menu item if it doesn't exist
        menu_item, created = MenuItem.get_or_create(__package__, self.title, linked_object=self, permission=self.permission)
        if self.category:
            menu = self.category.menu_item.submenu
            if not menu.contains(menu_item):
                # delete it from any other menus
                Menu.remove_item_from_all_menus(menu_item)
                # and add it last in the correct one
                menu.add_item(menu_item, menu.count())

    def delete(self, *args, **kwargs):
        MenuItem.delete_all_that_links_to(self)
        super(InfoPage, self).delete(*args, **kwargs)


class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
    author = models.ForeignKey(User)
    date = models.DateTimeField('Date edited')

