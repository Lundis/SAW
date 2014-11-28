from users.groups import GUEST, BOARD_MEMBER, LOGGED_ON

def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_comments", GUEST, "Can view comments on items with comments"),
        ("can_comment", LOGGED_ON, "Can comment on items with comments enabled"),
        ("can_force_comment", BOARD_MEMBER, "Can comment to items with comments disabled"),
    )