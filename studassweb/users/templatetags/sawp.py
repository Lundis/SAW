from django.template import Library
from users.permissions import has_user_perm
from base.utils import get_str_from_module
from base.register import FORCE_COMMENT
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
        logger.error("has_perm couldn't find %s in %s", perm_constant, app)
    user = context['user']
    return has_user_perm(user, perm)


@register.assignment_tag(takes_context=True)
def can_edit_object(context, obj):
    access = obj.can_edit(context['user'])
    logger.debug("can_edit_object(context, %s): %s", obj, access)
    return access


@register.assignment_tag(takes_context=True)
def can_view_object(context, obj):
    access = obj.can_view(context['user'])
    logger.debug("can_view_object(context, %s): %s", obj, access)
    if hasattr(obj, "permission"):
        logger.debug("user: %s, permission: %s", context['user'], obj.permission)
    return access


@register.assignment_tag(takes_context=True)
def can_view_comments(context, obj):
    access = obj.can_view_comments(context['user']) and obj.comments_enabled
    logger.debug("can_view_comments(context, %s): %s", obj, access)
    return access


@register.assignment_tag(takes_context=True)
def can_comment(context, obj):
    if not can_view_comments(context, obj):
        logger.debug("user %s cannot comment on %s (cannot read)", context['user'], obj)
        return False
    access = obj.can_comment(context['user']) and obj.comments_enabled
    logger.debug("can_view_object(context, %s): %s", obj, access)
    if hasattr(obj, "permission"):
        logger.debug("user: %s, permission: %s", context['user'], obj.permission)
    return access