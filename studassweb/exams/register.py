from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER


def get_menu_items():
    return ([MenuItem.get_or_create(__package__,
                                    "Exams",
                                    reverse_string="exams_main",
                                    permission=SAWPermission.get_or_create("can_view_events"))],
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
        ("can_view_exam_archive", GUEST, "Can view the exam archive"),
        ("can_upload_exams", MEMBER, "Can upload exams, add courses and examinators"),
        ("can_edit_exams", BOARD_MEMBER, "Can edit and delete exams and descriptions"),
    )