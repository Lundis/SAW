from .models import SAWPermission
from django.contrib.auth.models import Group
import logging

logger = logging.Logger(__name__)


def has_user_perm(user, perm_name):
    """
    :param user: User object
    :param perm_name: permission string
    """
    logger.debug("has_user_perm(%s, %s)", user, perm_name)
    try:
        sawp = SAWPermission.objects.get(permission__codename=perm_name)
    except SAWPermission.DoesNotExist:
        logger.error("Non-existing permission: %s", perm_name)
        return False
    return sawp.has_user_perm(user)


def add_perm_to_group(perm, group):
    """
    Adds a permission to a group and at the same time creates a SAWPermission if it doesn't exist.
    :param perm: A permission string
    :param group: Either an Actual Group object or a string
    """
    if isinstance(group, Group):
        group_instance = group
    else:
        group_instance = Group.objects.get(name=group)

    sawp = SAWPermission.get(perm)
    group_instance.permissions.add(sawp.permission)


def get_readable_perm(perm_codename):
    """
    Removes underscores and capitalizes the first letter of the argument and returns the result
    :param perm_codename:
    :return:
    """
    return perm_codename.replace("_", " ").capitalize()