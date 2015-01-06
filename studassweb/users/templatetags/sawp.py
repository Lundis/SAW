from django.template import Library
from users.permissions import has_user_perm
from base.utils import get_str_from_module
import logging

logger = logging.getLogger(__name__)

register = Library()


@register.assignment_tag(takes_context=True)
def has_perm(context, app, perm_constant):
    """
    Checks for perm_constant in app.register, and then checks if the current user has the permission.
    :param context:
    :param module:
    :param perm_constant:
    :return:
    """
    perm = get_str_from_module(app, "register", perm_constant)
    if perm is None:
        logger.error("has_perm couldn't find {0} in {1}", perm_constant, app)
    user = context['user']
    return has_user_perm(user, perm)


@register.assignment_tag(takes_context=True)
def can_edit_object(context, obj):
    logger.debug("can_edit_object(context, %s", obj)
    return obj.can_edit(context['user'])


@register.assignment_tag(takes_context=True)
def can_view_object(context, obj_str):
    obj = obj_str
    logger.debug("can_view_object(context, %s", obj)
    return obj.can_view(context['user'])