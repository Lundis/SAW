# coding=utf-8
from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def has_user_voted(context, poll):
    return poll.has_user_voted(context['user'], context['ip_address'])


@register.assignment_tag(takes_context=True)
def can_vote_object(context, poll):
    access = poll.can_user_vote(context['user'], context['ip_address'])
    return access
