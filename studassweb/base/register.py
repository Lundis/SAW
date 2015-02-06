from django.core.urlresolvers import reverse_lazy
from users.groups import GUEST, BOARD_MEMBER, LOGGED_ON, WEBMASTER
from settings.sections import Page, SECTION_APPEARANCE

VIEW_PUBLIC_COMMENTS = "can_view_public_comments"
VIEW_MEMBER_COMMENTS = "can_view_member_comments"
CAN_COMMENT = "can_comment"
FORCE_COMMENT = "can_force_comment"
EDIT_THEME = "can_edit_themes"
CAN_GIVE_FEEDBACK = "can_give_feedback"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (VIEW_PUBLIC_COMMENTS, GUEST, "Can view comments on items with public comments"),
        (VIEW_MEMBER_COMMENTS, GUEST, "Can view comments on items with member comments"),
        (CAN_COMMENT, LOGGED_ON, "Can comment on items with comments enabled.  This is further restricted by the view permissions for comments."),
        (FORCE_COMMENT, BOARD_MEMBER, "Can comment to items with comments disabled"),
        (EDIT_THEME, WEBMASTER, "Can change the overall theme of the site"),
        (CAN_GIVE_FEEDBACK, GUEST, "Can use feedback forms")
    )


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^base/",


def register_settings_pages():
    theme_editor = Page("Theme editor",
                        "Change the overall looks of the site",
                        SECTION_APPEARANCE,
                        reverse_lazy('base_settings_edit_theme'),
                        EDIT_THEME)
    return theme_editor,