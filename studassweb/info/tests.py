from django.test import TestCase
from .models import InfoPage, InfoCategory
from menu.models import MenuItem, Menu


class InfoCategoryTest(TestCase):

    def test_create_delete_category(self):
        """
        Tests that a menu item and a submenu is created and deleted along with the category
        """
        cat = InfoCategory.objects.create(name="category")

        # Now there should be a menu item for the category
        menu_item = MenuItem.get_all_that_links_to(cat)
        self.assertTrue(menu_item.count() == 1, "A single Menu item wasn't created")

        # The menu item should have a submenu
        submenu = menu_item[0].submenu
        self.assertIsNotNone(submenu, "Submenu wasn't created")

        # Let's delete the category
        cat.delete()

        # Was the submenu and the menu item deleted as well?
        try:
            menu = Menu.objects.get(menu_name=__package__ + "_category_" + cat.name)
            self.fail("Submenu exists after deletion")
        except Menu.DoesNotExist:
            pass

        try:
            menu_item = MenuItem.objects.get(app_name=__package__,
                                             display_name=cat.name)
            self.fail("Menu item exists after deletion")
        except MenuItem.DoesNotExist:
            pass


class InfoPageTest(TestCase):

    def setUp(self):
        self.category = InfoCategory.objects.create(name="category")

    def tearDown(self):
        self.category.delete()

    def test_create_delete_page(self):
        """
        Tests that a menu item is created and deleted along with the category
        """
        page = InfoPage.objects.create(title="test1",
                                       category=self.category,
                                       text="test_text")

        # Now there should be a menu item for the page
        menu_item = MenuItem.get_all_that_links_to(page)
        self.assertTrue(menu_item.count() == 1, "A single menu item wasn't created")

        # and it should've been added to the category menu
        menu = self.category.menu_item.submenu
        self.assertTrue(menu.contains(menu_item[0]), "The category menu does not contain the page")