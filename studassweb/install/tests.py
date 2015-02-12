from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .views import welcome, association, modules, menu, finished
from django.conf import settings
from menu.logic import get_all_menu_items
from base.models import SiteConfiguration

SUPERUSER_USERNAME = "install_superuser"
SUPERUSER_PASSWORD = "install_superuser"

ASSOCIATION_NAME = "Super association"
ASSOCIATION_FOUNDED = "1990"


class InstallHttpTests(TestCase):

    def setUp(self):
        #Setup test members/users
        self.superuser = User.objects.create_superuser(SUPERUSER_USERNAME, '', SUPERUSER_PASSWORD)
        self.factory = RequestFactory()

    def test_run_through_whole_install_process(self):
        #GET Welcome page
        request = self.factory.get(reverse("install.views.welcome"))
        request.user = self.superuser
        response = welcome(request)
        self.assertEqual(response.status_code, 200)

        #GET Association page
        request = self.factory.get(reverse("install.views.association"))
        request.user = self.superuser
        response = association(request)
        self.assertEqual(response.status_code, 200)

        #POST Association page
        request = self.factory.post(reverse("install.views.association"),
                                    {'name': ASSOCIATION_NAME, 'founded': ASSOCIATION_FOUNDED, })
        request.user = self.superuser
        response = association(request)
        #we should _maybe_ check that it redirects to the right page but it doesn't really work.
        #self.assertRedirects(response, reverse("install.views.modules"), fetch_redirect_response=False)
        self.assertEqual(response.status_code, 302)
        #Check that it's actually saved in DB
        site_config = SiteConfiguration.instance()
        self.assertEqual(site_config.association_name, ASSOCIATION_NAME)
        self.assertEqual(str(site_config.association_founded), ASSOCIATION_FOUNDED)

        #GET Modules page
        request = self.factory.get(reverse("install.views.modules"))
        request.user = self.superuser
        response = modules(request)
        self.assertEqual(response.status_code, 200)

        #POST Modules page
        #association=on&contact=on&events=on&exams=on&frontpage=on&gallery=on&info=on&news=on&polls=on
        all_modules = settings.OPTIONAL_APPS
        postdata = {}
        for module in all_modules:
            postdata[module] = 'on'
        request = self.factory.post(reverse("install.views.modules"), postdata, follow=True)
        request.user = self.superuser
        response = modules(request)
        self.assertEqual(response.status_code, 302)
        #TODO check that all modules are actually enabled

        #GET Menu page
        request = self.factory.get(reverse("install.views.menu"))
        request.user = self.superuser
        response = modules(request)
        self.assertEqual(response.status_code, 200)

        #POST Menu page
        # login_menu-menu-item-14=0&login_menu-menu-item-15=1&login_menu-menu-item-18=2&main_menu-menu-item-7=0&
        # main_menu-menu-item-8=1&main_menu-menu-item-9=2&main_menu-menu-item-10=3&main_menu-menu-item-11=4&
        # main_menu-menu-item-12=5&main_menu-menu-item-13=6&main_menu-menu-item-16=7&main_menu-menu-item-17=8

        menu_items, login_items, available_items = get_all_menu_items()
        i = 0
        postdata = {}
        for login_item in login_items:
            postdata["login_menu-item-"+str(login_item.id)] = i
            i += 1

        i = 0
        for menu_item in menu_items:
            postdata["main_menu-item-"+str(menu_item.id)] = i
            i += 1

        for available_item in available_items:
            postdata["main_menu-item-"+str(available_item.id)] = i
            i += 1

        request = self.factory.post(reverse("install.views.menu"), postdata)
        request.user = self.superuser
        response = menu(request)
        self.assertEqual(response.status_code, 302)
        #TODO check that the menu is saved correctly. This one might be hard(?)

        #GET Finished page
        request = self.factory.get(reverse("install.views.finished"))
        request.user = self.superuser
        response = finished(request)
        self.assertEqual(response.status_code, 200)