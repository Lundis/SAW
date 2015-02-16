from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

CAN_VIEW_EXAM_ARCHIVE = "can_view_exam_archive"
CAN_UPLOAD_EXAMS = "can_upload_exams"
CAN_EDIT_EXAMS = "can_edit_exams"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="exams_home",
                                           app_name=__package__,
                                           display_name="Exams",
                                           reverse_string="exams_main",
                                           permission=SAWPermission.get_or_create(CAN_VIEW_EXAM_ARCHIVE))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^exams/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW_EXAM_ARCHIVE, GUEST, "Can view the exam archive"),
        (CAN_UPLOAD_EXAMS, MEMBER, "Can upload exams, add courses and examinators"),
        (CAN_EDIT_EXAMS, BOARD_MEMBER, "Can edit and delete all exams, courses and examinators. " \
                                       "A user can always edit and delete stuff created by themselves"),
    )