from django.template import Library
from users.permissions import has_user_perm

register = Library()

@register.assignment_tag(takes_context=True)
def has_perm(context, perm):
    user = context['user']
    return has_user_perm(user, perm)