from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import SAWPermission
from base.models import DisabledModule
from .setup import PATH_CHOICES
from solo.models import SingletonModel
import logging

logger = logging.getLogger(__name__)


class MenuTemplate(models.Model):
    path = models.CharField(max_length=10, unique=True, blank=False, choices=PATH_CHOICES, default="standard")
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    uses_image = models.BooleanField(default=False)
    preview = models.ImageField(null=True)
    for_main_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    def create(cls, name, path, description, uses_image, for_main_menu=False):
        obj, created = cls.objects.get_or_create(path=path, name=name)
        if created:
            obj.description = description
            obj.for_main_menu = for_main_menu
            obj.uses_image = uses_image
            obj.save()
        return obj, created


class MainMenuSettings(SingletonModel):
    image = models.ImageField(upload_to="menu/images", null=True, blank=True)
    inverted_style = models.BooleanField(default=False, blank=True)

    @classmethod
    def is_menu_inverted(cls):
        return cls.instance().inverted_style

    @classmethod
    def instance(cls):
        return cls.objects.get_or_create()[0]

    def image_ratio(self):
        """
        :return: width/height of the image rounded to the closest integer. 1 if it doesn't exist
        """
        if self.image:
            return int(round(self.image.width / self.image.height, 0))
        else:
            return 1


TYPE_APP = 'AP'
TYPE_USER = 'US'
TYPE_CHOICES = (
    (TYPE_APP, "Created by app"),
    (TYPE_USER, "Created by user"),
)


class Menu(models.Model):
    menu_name = models.CharField(max_length=30, unique=True)
    template = models.ForeignKey(MenuTemplate, blank=True, null=True)
    # was the menu created by an app or a user?
    created_by = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_APP)

    def __str__(self):
        return self.menu_name

    def add_item(self, menu_item, index=None):
        """
        Add menu_item to this menu
        """
        if index is None:
            index = self.count()
        link = ItemInMenu(menu=self, item=menu_item, display_order=index)
        link.save()

    def remove_item(self, menu_item):
        """
        Remove menu_item from this menu
        """
        link = ItemInMenu.objects.get(menu=self, item=menu_item)
        link.delete()
        # reorder the remaining items
        index = 0
        for item in self.items():
            item.display_order = index
            index += 1
            item.save()

    @classmethod
    def remove_item_from_all_menus(cls, menu_item):
        """
        Remove menu_item from all menus
        """
        link = ItemInMenu.objects.filter(item=menu_item)
        if link:
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

    def contains(self, item):
        """
        :param item: MenuItem
        :return: true if this menu contains the menu item.
        """
        return ItemInMenu.objects.filter(menu=self, item=item).exists()

    @classmethod
    def get(cls, name):
        """
        Returns the menu if it exists, otherwise None
        TODO: remove
        """
        return cls.objects.get(menu_name=name)

    @classmethod
    def get_or_create(cls, name, template=None, created_by=TYPE_APP):
        """
        returns the menu, and updates it with the specified values
        :param name: unique identifier for the menu
        :param template: optional template used by the display_menu tag
        :return: requested menu, boolean (if it was created)
        """
        menu, created = cls.objects.get_or_create(menu_name=name)
        if template:
            menu.template = template
        menu.created_by = created_by
        menu.save()
        return menu, created


class MenuItem(models.Model):

    # app_name is used for checking if it belongs to a disabled module
    app_name = models.CharField(max_length=50, null=True, blank=True)
    identifier = models.CharField(max_length=100, unique=True,
                                  help_text="A unique identifier that is used to distinguish this item")
    display_name = models.CharField(max_length=30)

    # A field for referring to external URLs
    external_url = models.CharField(max_length=200, null=True, blank=True)
    # A field for getting a link using reverse()
    reverse_string = models.CharField(max_length=100, null=True, blank=True)
    # A generic field for linking to any model
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    link_target = GenericForeignKey('content_type', 'object_id')

    submenu = models.ForeignKey(Menu, null=True, blank=True)
    view_permission = models.ForeignKey(SAWPermission, null=True, blank=True)
    # was the menu created by an app or a user?
    created_by = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_APP)

    def __str__(self):
        url = self.url()
        if url is None:
            logger.error("Menu Item (%s) has no URL!", self.id)
        return self.identifier

    def clean(self):
        super(MenuItem, self).clean()
        if not self.url() and not self.submenu:
            raise ValidationError("Neither a URL nor a submenu has been selected")

    def was_created_by_user(self):
        return self.created_by == TYPE_USER

    @classmethod
    def get_or_create(cls, identifier, app_name=None, display_name=None, reverse_string=None,
                      linked_object=None, url=None, permission=None, submenu=None):
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
        menu_item, created = cls.objects.get_or_create(identifier=identifier)
        if not created:
            return menu_item, created
        menu_item.app_name = app_name
        menu_item.display_name = display_name

        if permission and isinstance(permission, str):
            permission = SAWPermission.get(perm_name=permission)

        if linked_object:
            if reverse_string or url:
                raise ValueError("reverse_string and/or url cannot be given at the same time as referred_item")
            content_type = ContentType.objects.get_for_model(linked_object)
            menu_item.content_type = content_type
            menu_item.object_id = linked_object.id

        elif reverse_string:
            if url:
                raise ValueError("url cannot be given at the same time as referred_item")
            menu_item.reverse_string = reverse_string
        elif url:
            menu_item.external_url = url
        else:
            raise ValueError("No url, reverse string or item was given to MenuItem.get_or_create()")

        if permission:
            menu_item.view_permission = permission

        if submenu:
            menu_item.submenu = submenu

        menu_item.save()
        return menu_item, created

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
            return self.external_url

    @classmethod
    def get_all_that_links_to(cls, link_target):
        """
        Deletes all MenuItem that links to the target, and also any submenus owned by these items.
        :param link_target: target model
        """
        content_type = ContentType.objects.get_for_model(link_target)
        items = cls.objects.filter(content_type=content_type, object_id=link_target.id)
        return items

    @classmethod
    def delete_all_that_links_to(cls, link_target):
        """
        Deletes all MenuItem that links to the target, and also any submenus owned by these items.
        :param link_target: target model
        """
        items = cls.get_all_that_links_to(link_target)
        print(items)
        for item in items:
            item.delete()
            if item.submenu:
                item.submenu.delete()

    @classmethod
    def get_all_custom_items(cls):
        return cls.objects.filter(created_by=TYPE_USER)

    @classmethod
    def remove_disabled_items(cls):
        enabled_modules = DisabledModule.get_all_enabled_modules()
        # delete all items that have a non-empty app_name that doesn't point to an active module
        disabled_items = cls.objects.filter(~Q(app_name__in=enabled_modules),
                                            ~Q(app_name__isnull=True),
                                            ~Q(app_name=""))
        disabled_items.delete()


class ItemInMenu(models.Model):
    """
    Connects Menu and MenuItem. Don't use directly. Use Menu.add_item() or Menu.remove_item()
    """
    menu = models.ForeignKey(Menu)
    item = models.ForeignKey(MenuItem)
    display_order = models.IntegerField()

    class Meta:
        unique_together = (('menu', 'item'),
                           ('menu', 'display_order'))
        ordering = ['menu', 'display_order']

    def __str__(self):
        return self.item.display_name + " in " + self.menu.menu_name