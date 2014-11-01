from django.db import models

class MenuTemplate(models.Model):
    path = models.CharField(max_length=100, unique=True)

    @classmethod
    def default(cls):
        return cls.objects.get_or_create(path__exact="menu/menu.html")


class Menu(models.Model):
    menu_name = models.CharField(max_length=30, unique=True)
    template = models.ForeignKey(MenuTemplate, blank=True, null=True)

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


class MenuItem(models.Model):

    #app_name is used for checking if it belongs to a disabled module
    app_name = models.CharField(max_length=50, null=True, blank=True)
    display_name = models.CharField(max_length=30)
    # TODO: should url be unique?
    url = models.URLField()
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

    class Meta:
        # Don't allow duplicates
        unique_together = ('display_name', 'url')

    @classmethod
    def get_or_create(cls, app_name, display_name, url, default_menu=NONE):
        """
        Shortcut function for MenuItem.objects.get_or_create
        """
        item, created = cls.objects.get_or_create(app_name=app_name,
                                                  display_name=display_name,
                                                  url=url,
                                                  default_menu=default_menu)
        return item


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