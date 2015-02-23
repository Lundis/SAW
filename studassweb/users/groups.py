from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _
from base.utils import get_modules_with
from .models import SAWPermission
import logging

logger = logging.Logger(__name__)

GUEST = "Guest"
LOGGED_ON = "Registered"
MEMBER = "Member"
BOARD_MEMBER = "Board Member"
WEBMASTER = "Webmaster"

# the list of groups in hierarchical order
group_names = [GUEST, LOGGED_ON, MEMBER, BOARD_MEMBER, WEBMASTER]


GROUP_CHOICES = ((GUEST, _(GUEST)),
                 (LOGGED_ON, _(LOGGED_ON)),
                 (MEMBER, _(MEMBER)),
                 (BOARD_MEMBER, _(BOARD_MEMBER)),
                 (WEBMASTER, _(WEBMASTER)))


def setup_default_groups_and_permissions():
    """
    Creates all permissions and sets up all groups
    :return:
    """
    permission_funcs = get_modules_with("register", "get_permissions")
    # get all the groups from the database
    groups = [group for group, created in
              [Group.objects.get_or_create(name=group_name) for group_name in group_names]]
    for module, get_perms in permission_funcs:
        perms = get_perms()
        for perm, group, description in perms:
            # create the permission if it doesn't exist:
            SAWPermission.get_or_create(perm, group, description, module)
            # ignore permissions that already are in a group.
            # we don't want duplicates and we don't want to ruin changes made by the user.
            if not is_perm_in_groups(perm, groups):
                group_index = -1
                try:
                    group_index = group_names.index(group)
                except ValueError:
                    raise ValueError("Permission \"" +
                                     perm +
                                     "\" wants to join a non-existing default group \"" +
                                     group + "\"")
                if group_index != -1:
                    _add_perm_to_group(perm, groups[group_index])


def is_perm_in_groups(perm, groups):
    for group in groups:
        if group.permissions.filter(codename=perm).exists():
            return True
    return False


def get_permissions_in_group(group):
    """
    :param group: a group name or an actual Group
    :return: a list of permissions (SAWPermission) in this group.
    """
    if not isinstance(group, Group):
        group = Group.objects.get(name=group)
    all_perms = SAWPermission.objects.all()
    perms = [sawp.permission.id for sawp in all_perms]
    perms_in_group = group.permissions.filter(id__in=perms)
    # iterate though the SAWPermissions: return only the ones in the group
    return [perm for perm in all_perms if perm.permission in perms_in_group]


def put_user_in_standard_group(user, new_group_name):
    """
    This function puts the user in one of the default groups
    :param new_group_name: one of the default groups
    :param user: User
    :return:
    """
    if new_group_name not in group_names:
        raise ValueError("new_group_name \"" + new_group_name + "\" is not a default new_group_name")
    # remove old groups
    user_old_groups = user.groups.filter(name__in=group_names)
    for old_group in user_old_groups:
        user.groups.remove(old_group)
    # add user to all groups up to the specified one
    for group_name in group_names:
        group_inst = Group.objects.get(name=group_name)
        user.groups.add(group_inst)
        # stop when we've hit the specified one
        if group_name == new_group_name:
            break
    # Give webmasters access to the admin pages
    if new_group_name == WEBMASTER:
        user.is_staff = True
    else:
        user.is_staff = False
    user.save()


def _add_perm_to_group(perm, group):
    """
    Adds a permission to a group.
    :param perm: A permission string
    :param group: Either an Actual Group object or a string
    """
    if isinstance(group, Group):
        group_instance = group
    else:
        group_instance = Group.objects.get(name=group)

    sawp = SAWPermission.get(perm)
    group_instance.permissions.add(sawp.permission)


def get_standard_group_of_perm(perm):
    """
    :param perm: SAWPermission, Permission or string
    :return: the name (str) of the standard group the permission belongs to, or None if it doesn't belong to anything
    """
    if isinstance(perm, SAWPermission):
        perm = perm.permission
    elif isinstance(perm, str):
        perm = SAWPermission.get(perm).permission
    # else assume it's a Permission

    # iterate through them in reverse
    for group_name in group_names:
        group = Group.get(name=group_name)
        # TODO: this is a pretty inefficient query
        if perm in group.permissions.all():
            return group.name
    # If it's not in any of the default groups:
    return None


def get_user_group(user):
    """
    Returns the default group this user is in
    :param user:
    :return: Group name
    """
    for group in reversed(group_names):
        if user.groups.filter(name=group).exists():
            return group
    logger.error("User %s is not in any default group", user)
    return None