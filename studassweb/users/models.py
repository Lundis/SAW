from django.db import models
from django.contrib.auth.models import User, Permission, ContentType, Group
from solo.models import SingletonModel
import members.models
import random


def _generate_email_ver_code():
        code = ""
        alphabet = "qwertyuiopasdfghjklzxcvbnm1234567890"
        for i in range(32):
            code += alphabet[random.randint(0, len(alphabet)-1)]
        return code


class UserExtension(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/avatars', default='users/avatars/default_avatar.png')
    # A field where the user can write a short text about themselves
    description = models.TextField(max_length=1000, blank=True, default="")
    link_to_homepage = models.URLField(blank=True, default="")
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=32, unique=True)
    can_apply_for_membership = models.BooleanField(default=True)

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
        user_ext.email_verification_code = _generate_email_ver_code()
        while cls.objects.filter(email_verification_code=user_ext.email_verification_code).exists():
            user_ext = _generate_email_ver_code()
        user_ext.save()
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

    def member(self):
        try:
            return members.models.Member.objects.get(user=self.user)
        except members.models.Member.DoesNotExist:
            return None


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

    def __str__(self):
        return self.permission.codename

    @classmethod
    def get_or_create(cls, perm_name, description=None):
        """
        :return: The requested SAWPermission
        """
        fancy_name = perm_name[0].upper() + perm_name[1:].replace("_", " ")
        permission, created = Permission.objects.get_or_create(name=fancy_name,
                                                               codename=perm_name,
                                                               content_type=DummyPermissionBase.get_content_type())
        saw_permission, created = cls.objects.get_or_create(permission=permission)
        # if the description isn't "" and the object was created or it doesn't have a description, add the description
        if description and (created or not saw_permission.description):
            saw_permission.description = description
            saw_permission.save()
        return saw_permission

    def has_user_perm(self, user):
        """
        :return: True if the user has this permission
        """
        guest_group, created = Group.objects.get_or_create(name="Guest")
        is_guest_permission = guest_group.permissions.filter(pk=self.permission.pk)
        return user.is_superuser or is_guest_permission or \
               user.has_perm(self.permission.content_type.app_label + "." + self.permission.codename)


class DummyPermissionBase(SingletonModel):
    """
    This is used as base for our custom permissions
    """

    @classmethod
    def get_content_type(cls):
        return ContentType.objects.get(app_label="users", model="dummypermissionbase")