from django.db import models
from users.models import SAWPermission

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
    url = models.URLField()
    submenu = models.ForeignKey(Menu, null=True)
    # Does the item by default belong to a menu?
    # This is used to improve the usability of the installation wizard.
    MAIN_MENU = 'MM'
    LOGIN_MENU = 'LM'
    NONE = 'NO'
    MENU_CHOICES = (
        (MAIN_MENU, "Main menu"),
        (LOGIN_MENU, "Login menu"),
        (NONE, "No menu"),
    )
    default_menu = models.CharField(max_length=2, choices=MENU_CHOICES)
    view_permission = models.ForeignKey(SAWPermission, null=True, blank=True)

    class Meta:
        # Don't allow duplicates
        unique_together = ('display_name', 'url')

    def __str__(self):
        return self.display_name + ": " + self.url

    @classmethod
    def get_or_create(cls, app_name, display_name, url, default_menu=NONE, permission=None, submenu=None):
        """
        Shortcut function for MenuItem.objects.get_or_create
        :param app_name: Which app created this item (if any)
        :param display_name:  The string that is shown to the user
        :param url: URL
        :param default_menu: The default menu this item belongs to
        :param permission: The permission required to view this item. if None, anyone can view it
        :return:
        """
        item, created = cls.objects.get_or_create(app_name=app_name,
                                                  display_name=display_name,
                                                  url=url,
                                                  submenu=submenu)
        if created:
            item.default_menu = default_menu
            item.view_permission = permission
            item.save()
        return item

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
        return self.submenu != None


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