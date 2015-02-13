from django import template

register = template.Library()


@register.assignment_tag
def has_user_voted(poll, request):
    return poll.has_user_voted(request)