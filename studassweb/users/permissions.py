from .models import SAWPermission
from django.contrib.auth.models import Group


def has_user_perm(user, perm_name):
    """
    :param user: User object
    :param perm_name: permission string
    """
    sawp = SAWPermission.objects.get(permission__codename=perm_name)
    return sawp.has_user_perm(user)


def add_perm_to_group(perm, group):
    """
    Adds a permission to a group and at the same time creates a SAWPermission if it doesn't exist.
    :param perm:
    :param group: Either an Actual Group object or a string
    """
    if isinstance(group, Group):
        group_instance = group
    else:
        group_instance = Group.objects.get(name=group)

    sawp = SAWPermission.get_or_create(perm)
    group_instance.permissions.add(sawp.permission)