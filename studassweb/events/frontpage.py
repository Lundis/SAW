# coding=utf-8
from .models import Event
from django.template import Context
from django.template.loader import get_template


def render_upcoming_events(context) -> str:
    events = Event.current_events().order_by("start")
    events_dict = {
        'count': 0,
        'list': []
    }
    for event in events:
        if event.user_can_view_and_join(context['user']):
            events_dict['count'] += 1
            events_dict['list'].append(event)

    context['events'] = events_dict
    template = get_template("events/frontpage_content.html")
    return template.render(Context(context))
