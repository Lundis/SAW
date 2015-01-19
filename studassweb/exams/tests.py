from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from .models import Course, Examinator, SingleExam, ExamFile
from django.contrib.auth.models import User
from .views import add_edit_exam
from .register import get_menu_items
from studassweb.urls import urlpatterns
from django.contrib.auth.models import AnonymousUser, User
from users.models import UserExtension
from users.groups import setup_default_groups
from users.groups import put_user_in_default_group, MEMBER
from unittest import skip

from django.conf.urls import include, patterns, url

SUPERUSER_USERNAME = "examssuperuser"
SUPERUSER_PASSWORD = "examssuperuser"

MEMBER_USERNAME = "examsmember"
MEMBER_PASSWORD = "examsmember"


class ExamsHttpTests(TestCase):

    def setUp(self):
        #Here we should run the whole install process...
        #TODO we need to be able to run install from code
        setup_default_groups() # Create default user groups
        #get_menu_items() #Create default menu items... No we don't want to do this for every single application.fuck.

        #Setup test members/users
        self.superuser = User.objects.create_superuser(SUPERUSER_USERNAME, '', SUPERUSER_PASSWORD)
        self.memberuser = User.objects.create_user(MEMBER_USERNAME, '', MEMBER_PASSWORD)
        user_ext = UserExtension.create_for_user(self.memberuser)
        user_ext.email_verified = True
        user_ext.save()
        put_user_in_default_group(self.memberuser, MEMBER)
        self.factory = RequestFactory()

    def test_anonymous_can_not_add_course(self):
        request = self.factory.post(reverse("exams_add_course"), {'name': 'Datornätverk',})
        request.user = AnonymousUser()
        response = add_edit_exam(request)
        self.assertEqual(response.status_code, 403)

    @skip("We need to be able to run install process before this\n")
    def test_member_can_add_course(self):
        request = self.factory.post(reverse("exams_add_course"), {'name': 'Datornätverk',})
        request.user = User.objects.get_by_natural_key(MEMBER_USERNAME)
        response = add_edit_exam(request)
        #print(response.content)
        self.assertEqual(response.status_code, 200)

