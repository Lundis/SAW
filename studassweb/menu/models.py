from django.db import models
from users.models import SAWPermission
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class MenuTemplate(models.Model):
    path = models.CharField(max_length=100, unique=True)

    @classmethod
    def default(cls):
        obj, created = cls.objects.get_or_create(path="menu/menu.html")
        return obj

    def __str__(self):
        return self.path


class Menu(models.Model):
    menu_name = models.CharField(max_length=30, unique=True)
    template = models.ForeignKey(MenuTemplate, blank=True, null=True)

    def __str__(self):
        return self.menu_name

    def add_item(self, menu_item, index):
        """
        Add menu_item to this menu
        """
        print(self.menu_name, " adding item ", menu_item.display_name, "on index ", index)
        link = ItemInMenu(menu=self, item=menu_item, display_order=index)
        link.save()

    def remove_item(self, menu_item, index):
        """
        Remove menu_item from this menu
        """
        link = ItemInMenu.objects.get(menu=self, item=menu_item, display_order=index)
        link.delete()

    def clear(self):
        """
        Removes all items from this menu
        """
        items = ItemInMenu.objects.filter(menu=self)
        items.delete()

    def items(self, user=None):
        return [item_in_menu.item for
                item_in_menu in
                ItemInMenu.objects.filter(menu=self)
                if not user or item_in_menu.item.can_user_view(user)]

    def count(self):
        return ItemInMenu.objects.filter(menu=self).count()

    @classmethod
    def get_or_none(cls, name):
        """
        Returns the menu if it exists, otherwise None
        """
        try:
            return cls.objects.get(menu_name=name)
        except cls.DoesNotExist:
            return None


class MenuItem(models.Model):

    #app_name is used for checking if it belongs to a disabled module
    app_name = models.CharField(max_length=50, null=True, blank=True)
    display_name = models.CharField(max_length=30)
    # A field for referring to external URLs
    external_url = models.URLField(null=True, blank=True)
    # A field for getting a link using reverse()
    reverse_string = models.CharField(max_length=100, null=True, blank=True)
    # A generic field for linking to any model
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    link_target = GenericForeignKey('content_type', 'object_id')

    submenu = models.ForeignKey(Menu, null=True)
    view_permission = models.ForeignKey(SAWPermission, null=True, blank=True)
    # is the item managed by a specific app (referred to in app_name,
    # or is it a custom item created by the user.
    # I use choices instead of a boolean because it's clearer and more types might be added in the future.
    TYPE_APP = 'AP'
    TYPE_USER = 'US'
    TYPE_CHOICES = (
        (TYPE_APP, "Created by app"),
        (TYPE_USER, "Created by user"),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_APP)

    class Meta:
        # Don't allow duplicates
        unique_together = ('app_name', 'display_name')

    def __str__(self):
        return self.display_name + ": " + self.url()

    def clean(self, *args, **kwargs):
        super(MenuItem, self).clean(*args, **kwargs)
        if not self.url and not self.reverse_string and not self.item:
            raise ValidationError("no link defined for the menu item")

    def save(self, *args, **kwargs):
        self.clean()
        super(MenuItem, self).save(*args, **kwargs)

    @classmethod
    def get_or_create(cls, app_name, display_name, reverse_string=None, linked_object=None, url=None, permission=None, submenu=None):
        """
        Convenience wrapper to create or get valid menu items
        :param app_name: Which app created this item (if any)
        :param display_name:  The string that is shown to the user
        :param reverse_string: a string that can be called by Django's reverse() function to get a URL
        :param linked_object: a Django model with a get_absolute_url() method
        :param url: URL
        :param permission: The permission required to view this item. if None, anyone can view it
        :return:
        """
        menu_item = None
        created = False
        if permission and isinstance(permission, str):
            permission = SAWPermission.get_or_create(perm_name=permission)

        if linked_object:
            if reverse_string or url:
                raise ValueError("reverse_string and/or url cannot be given at the same time as referred_item")
            content_type = ContentType.objects.get_for_model(linked_object)
            menu_item, created = cls.objects.get_or_create(app_name=app_name,
                                                           display_name=display_name,
                                                           content_type=content_type,
                                                           object_id=linked_object.id)
        elif reverse_string:
            if url:
                raise ValueError("url cannot be given at the same time as referred_item")
            menu_item, created = cls.objects.get_or_create(app_name=app_name,
                                                           display_name=display_name,
                                                           reverse_string=reverse_string)
        elif url:
            menu_item, created = cls.objects.get_or_create(app_name=app_name,
                                                           display_name=display_name,
                                                           external_url=url)
        else:
            raise ValueError("No url, reverse string or item was given to MenuItem.get_or_create()")

        if created:
            menu_item.view_permission = permission
            menu_item.submenu = submenu
            menu_item.save()
        return menu_item

    @classmethod
    def get_defaults(cls, menu_id):
        """
        The main and login menus can have default items assigned to them.
        :param cls:
        :param menu_id: MAIN_MENU, LOGIN_MENU or NONE
        :return: A QuerySet of the default menu items.
        """
        return cls.objects.filter(default_menu=menu_id)

    def can_user_view(self, user):
        """
        :return: True if this item has no associated permission or if the user has the permission
        """
        return not self.view_permission or self.view_permission.has_user_perm(user)

    def has_submenu(self):
        return self.submenu is not None

    def url(self):
        if self.link_target:
            return self.link_target.get_absolute_url()
        elif self.reverse_string:
            return reverse(self.reverse_string)
        else:
            return self.url


class ItemInMenu(models.Model):
    """
    Connects Menu and MenuItem. Don't use directly. Use Menu.add_item() or Menu.remove_item()
    """
    menu = models.ForeignKey(Menu)
    item = models.ForeignKey(MenuItem)
    display_order = models.IntegerField()

    class Meta:
        unique_together = ('menu', 'item')
        ordering = ['menu', 'display_order']

    def __str__(self):
        return self.item + " in " + self.menu