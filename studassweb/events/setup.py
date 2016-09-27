# coding=utf-8
import events.models as emodels
from frontpage.models import FrontPageItem
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils.timezone import datetime, timedelta
from .register import CAN_VIEW_AND_JOIN_PUBLIC_EVENTS


def setup():
    esettings = emodels.EventSettings.instance()
    if not esettings.is_setup:
        # set up some event items
        diet_item = emodels.EventItem(name="Diet",
                                      required=False,
                                      public=False,
                                      hide_in_print_view=False,
                                      type=emodels.EventItem.TYPE_STR,
                                      )
        diet_item.save()
        assoc_item = emodels.EventItem(name="Association",
                                       required=False,
                                       public=True,
                                       hide_in_print_view=False,
                                       type=emodels.EventItem.TYPE_STR,
                                       )
        assoc_item.save()

        # Then create an example event
        event = emodels.Event(title=_("Website birth celebration"),
                              text="<p>" + _("Celebrate the creation of this website with your friends!") + "</p>",
                              start=datetime.now(),
                              stop=datetime.now() + timedelta(days=7),
                              signup_start=datetime.now(),
                              signup_deadline=datetime.now() + timedelta(days=7),
                              permission=CAN_VIEW_AND_JOIN_PUBLIC_EVENTS,
                              max_participants=50,
                              author=User.objects.all().first())
        event.save()
        # Add the event items to it
        emodels.ItemInEvent(event=event, item=diet_item).save()
        emodels.ItemInEvent(event=event, item=assoc_item).save()

        # Mark the module as set up
        esettings.is_setup = True
        esettings.save()

    # Make sure that the new frontpage item exists
    item, created = FrontPageItem.objects.get_or_create(identifier="events/upcoming_events_v2")
    if created:
        item.title = "Upcoming Events"
        item.module = "events"
        item.render_function = "render_upcoming_events"
        item.save()

