from django.template import Library

register = Library()


@register.assignment_tag()
def setvar(value):
    return value