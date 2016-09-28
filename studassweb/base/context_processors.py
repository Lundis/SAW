# coding=utf-8
from django.conf import settings


def saw_version(request):
    """
    Add SAW_VERSION to the template context
    :param request:
    :return:
    """
    return {
        'SAW_VERSION': settings.SAW_VERSION
    }
