# coding=utf-8
from django import template

register = template.Library()


@register.simple_tag()
def setvar(value):
    """

    :param value:
    :return:
    """
    return value
