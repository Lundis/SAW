from django import template

register = template.Library()


@register.assignment_tag
def has_user_voted(poll, request):
    return poll.has_user_voted(request)


@register.assignment_tag
def can_vote_object(poll, request):
    access = poll.can_user_vote(request)
    return access