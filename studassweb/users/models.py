from django.db import models
from django.contrib.auth.models import User, Permission, ContentType, Group
from solo.models import SingletonModel
from members.models import Member
from base.utils import IllegalArgumentException


class UserExtension(models.Model):
    user = models.ForeignKey(User)
    # A field where the user can write a short text about themselves
    description = models.TextField(max_length=1000, blank=True, default="")
    link_to_homepage = models.URLField(blank=True, default="")
    member = models.ForeignKey(Member, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def create_user(cls, username, password, first_name, last_name, email,
                    member=False, enrollment_year=None, graduation_year=0):
        """
        :return:
        """
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user_ext = UserExtension(user=user)
        if member:
            if not enrollment_year:
                raise IllegalArgumentException("if the user is a member, enrollment year must be specified")
            if not graduation_year:
                graduation_year = 0
            _member = Member(enrollment_year=enrollment_year, graduation_year=graduation_year)
            _member.save()
            user_ext.member = _member
        user_ext.save()
        return user_ext




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