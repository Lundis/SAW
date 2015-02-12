from django import template

register = template.Library()


@register.assignment_tag
def user_can_edit(signup, user):
    return signup.user_can_edit(user)