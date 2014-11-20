from users.groups import WEBMASTER


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_force_comment", WEBMASTER, "Can change the menu layout"),
    )