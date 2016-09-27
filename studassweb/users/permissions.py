# coding=utf-8
from .models import SAWPermission
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


def get_readable_perm(perm_codename):
    """
    Removes underscores and capitalizes the first letter of the argument and returns the result
    :param perm_codename:
    :return:
    """
    return perm_codename.replace("_", " ").capitalize()
