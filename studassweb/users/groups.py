from django.contrib.auth.models import Group, User
from base.utils import IllegalArgumentException, get_modules_with
from users.permissions import add_perm_to_group
from .models import SAWPermission

GUEST = "Guest"
LOGGED_ON = "Logged On"
MEMBER = "Member"
BOARD_MEMBER = "Board Member"
WEBMASTER = "Webmaster"

# the list of groups in hierarchical order
group_names = [GUEST, LOGGED_ON, MEMBER, BOARD_MEMBER, WEBMASTER]


def setup_default_groups():
    permission_funcs = [func for module, func in get_modules_with("register", "get_permissions")]
    # get all the groups from the database
    groups = [group for group, created in
              [Group.objects.get_or_create(name=group_name) for group_name in group_names]]
    for get_perms in permission_funcs:
        perms = get_perms()
        for perm, group, description in perms:
            # create the permission if it doesn't exist:
            SAWPermission.get_or_create(perm, description)
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
                    add_perm_to_group(perm, groups[group_index])


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


def put_user_in_default_group(user, group):
    """
    This function puts the user in one of the default groups
    :param group: one of the default groups
    :param user: User
    :return:
    """
    if group not in group_names:
        raise IllegalArgumentException("group \"" + group + "\" is not a default group")
    # remove old groups
    user_old_groups = user.groups.filter(name__in=group_names)
    for old_group in user_old_groups:
        user.groups.remove(old_group)
    # add user to all groups up to the specified one
    for group_name in group_names:
        group_inst = Group.objects.get(name=group_name)
        user.groups.add(group_inst)
        # stop when we've hit the specified one
        if group_name == group:
            break
    # Give access to the admin pages to webmasters
    if group == WEBMASTER:
        user.is_staff = True
    else:
        user.is_staff = False
    user.save()