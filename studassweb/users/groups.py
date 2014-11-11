from django.contrib.auth.models import Group
from base.utils import IllegalArgumentException, get_modules_with
from users.models import SAWPermission

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
        for perm, group in perms:
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
                    SAWPermission.add_perm_to_group(perm, groups[group_index])


def is_perm_in_groups(perm, groups):
    for group in groups:
        if group.permissions.filter(codename=perm).exists():
            return True
    return False


def put_user_in_default_group(user, group):
    """
    This function puts the user in one of the default groups
    :param group: one of the default groups
    :param user: User
    :return:
    """
    if group not in group_names:
        raise IllegalArgumentException("group " + group + " is not a default group")
    pass