from users.groups import GUEST, BOARD_MEMBER, LOGGED_ON, WEBMASTER
from menu.models import MenuItem
from users.models import SAWPermission

VIEW_COMMENTS = "can_view_comments"
CAN_COMMENT = "can_comment"
FORCE_COMMENT = "can_force_comment"
EDIT_THEME = "can_edit_themes"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (VIEW_COMMENTS, GUEST, "Can view comments on items with comments"),
        (CAN_COMMENT, LOGGED_ON, "Can comment on items with comments enabled"),
        (FORCE_COMMENT, BOARD_MEMBER, "Can comment to items with comments disabled"),
        (EDIT_THEME, WEBMASTER, "Can change the overall theme of the site")
    )


def get_settings_items():
    item, created = MenuItem.get_or_create(__package__,
                                           'Theme',
                                           reverse_string='base_settings_edit_theme',
                                           permission=SAWPermission.get_or_create(EDIT_THEME))
    return [item]