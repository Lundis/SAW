from django.db import models
from django.contrib.auth.models import User, Permission, ContentType, Group
from solo.models import SingletonModel
from base.models import DisabledModule
from importlib import import_module
import users.groups
import logging
from base.utils import generate_email_ver_code

logger = logging.getLogger(__name__)


class UserExtension(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/avatars', default='users/avatars/default_avatar.png')
    # A field where the user can write a short text about themselves
    description = models.TextField(max_length=1000, blank=True, default="")
    link_to_homepage = models.URLField(blank=True, default="")
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def create_user(cls, username, password, first_name, last_name, email):
        """
        :return:
        """
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return cls.create_for_user(user)

    @classmethod
    def create_for_user(cls, user):
        user_ext = UserExtension(user=user)
        # make sure the verification code is unique
        user_ext.email_verification_code = generate_email_ver_code()
        while cls.objects.filter(email_verification_code=user_ext.email_verification_code).exists():
            user_ext = generate_email_ver_code()
        user_ext.save()
        # Create a member object for superusers if the members module is enabled
        if DisabledModule.is_enabled("members"):
            # dynamic import to get rid of dependency
            members = import_module("members.models")
            members.Member.create_from_user_ext(user_ext)
            logger.warning('Member for user %s was created at login' % user.username)
        return user_ext

    @classmethod
    def verify_email(cls, code):
        try:
            user_ext = cls.objects.get(email_verification_code=code)
            user_ext.email_verified = True
            user_ext.save()
            return True
        except cls.DoesNotExist:
            return False

    def groups(self):
        """
        Returns any groups this user is in. Only the most import default group is returned.
        TODO: also return custom groups
        :return:
        """
        return users.groups.get_user_group(self.user),


class LdapLink(models.Model):
    user = models.ForeignKey(User)
    hostname = models.CharField(max_length=200)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username + ": " + self.username + "@" + self.hostname


class SAWPermission(models.Model):
    """
    This model wraps Django's built-in Permission object, providing a description.
    """
    permission = models.ForeignKey(Permission, primary_key=True)
    description = models.CharField(max_length=200)
    default_group = models.ForeignKey(Group, null=True, default=None)
    module = models.CharField(max_length=100)

    def __str__(self):
        return self.permission.codename

    @classmethod
    def get(cls, perm_name):
        """
        :param perm_name: The name of the permission (str)
        :return:
        """
        perm = Permission.objects.get(codename=perm_name)
        try:
            return cls.objects.get(permission=perm)
        except cls.DoesNotExist:
            logger.error("SAWPermission \"%s\" does not exist!", perm.codename)

    @classmethod
    def get_or_create(cls, perm_name, default_group, description, module):
        """

        :param perm_name: name of permission (str)
        :param default_group: A Group or a string
        :param description:
        :param module:
        :return:
        """
        if not isinstance(default_group, Group):
            default_group = Group.objects.get(name=default_group)
        fancy_name = perm_name[0].upper() + perm_name[1:].replace("_", " ")
        permission, created = Permission.objects.get_or_create(name=fancy_name,
                                                               codename=perm_name,
                                                               content_type=DummyPermissionBase.get_content_type())
        logger.info("Created permission %s", perm_name)
        saw_permission, created = cls.objects.get_or_create(permission=permission)
        if module:
            saw_permission.module = module
        if description:
            saw_permission.description = description
        if default_group:
            saw_permission.default_group = default_group
        if description or default_group or module:
            saw_permission.save()
        return saw_permission

    def has_user_perm(self, user):
        """
        :return: True if the user has this permission
        """
        guest_group, created = Group.objects.get_or_create(name=users.groups.GUEST)
        is_guest_permission = guest_group.permissions.filter(pk=self.permission.pk).exists()
        logger.debug("\"%s\" is guest permission? %s" % (self.permission.codename, is_guest_permission))
        return user.is_superuser or is_guest_permission or \
               user.has_perm(self.permission.content_type.app_label + "." + self.permission.codename)


class DummyPermissionBase(SingletonModel):
    """
    This is used as base for our custom permissions
    """

    @classmethod
    def get_content_type(cls):
        return ContentType.objects.get(app_label="users", model="dummypermissionbase")