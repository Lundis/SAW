from users.groups import GUEST, BOARD_MEMBER, LOGGED_ON

def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_comments", GUEST),
        ("can_comment", LOGGED_ON),
        ("can_force_comment", BOARD_MEMBER),
    )