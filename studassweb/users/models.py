from django.db import models
from django.contrib.auth.models import User, Permission, ContentType
from solo.models import SingletonModel

class UserExtension(models.Model):
    user = models.ForeignKey(User)
    # A field where the user can write a short text about themselves
    description = models.TextField(max_length=1000)
    link_to_homepage = models.CharField(max_length=400)


class LdapLink(models.Model):
    user = models.ForeignKey(User)
    hostname = models.CharField(max_length=200)
    username = models.CharField(max_length=50)


class SAWPermission(models.Model):
    """
    This model wraps Django's built-in Permission object, providing a description.
    """
    permission = models.ForeignKey(Permission, primary_key=True)
    description = models.CharField(max_length=200)

    @classmethod
    def get_or_create(cls, perm_name, description=None):
        """
        :return: The requested SAWPermission
        """
        permission, created = Permission.objects.get_or_create(name=perm_name,
                                                                    code_name=perm_name,
                                                                    content_type=DummyPermissionBase)
        saw_permission, created = cls.objects.get_or_create(permission=permission)
        if description and (created or not saw_permission.description):
            saw_permission.description = description
            saw_permission.save()
        return saw_permission

    def has_user_perm(self, user):
        """

        :return: True if the user has this permission
        """
        return user.has_perm(self.permission.content_type.app_label + "." + self.permission.code_name)

    @classmethod
    def has_user_perm(cls, user, perm_name):
        """
        :param user: User object
        :param perm_name: Permission string
        """
        sawp = cls.get_or_create(perm_name)
        return sawp.has_user_perm(perm_name)


class DummyPermissionBase(SingletonModel):
    """
    This is used as base for our custom permissions
    """

    @classmethod
    def get_content_type(cls):
        return ContentType.get_for_model(cls)