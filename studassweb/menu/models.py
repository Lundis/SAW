from django.db import models

class Menu(models.Model):
    menu_name = models.CharField(max_length=30, unique=True)
    template = models.CharField(max_length=100)

    def add_item(self, menu_item, order):
        """
        Add menu_item to this menu
        """
        link = ItemInMenu(menu=self, item=menu_item, display_order=order)
        link.save()

    def remove_item(self, menu_item, order):
        """
        Remove menu_item from this menu
        """
        link = ItemInMenu.objects.get(menu=self, item=menu_item, display_order=order)
        link.delete()

    def clear(self):
        """
        Removes all items from this menu
        """
        ItemInMenu.objects.filter()


class MenuItem(models.Model):
    app_name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)

    class Meta:
        unique_together = ('app_name', 'display_name', 'url')


class ItemInMenu(models.Model):
    """
    Connects Menu and MenuItem. Don't use directly. Use Menu.add_item() or Menu.remove_item()
    """
    menu = models.ForeignKey(Menu)
    item = models.ForeignKey(MenuItem)
    display_order = models.IntegerField(default=0)

    class Meta:
        unique_together = ('menu', 'item')
        ordering = ['display_order']