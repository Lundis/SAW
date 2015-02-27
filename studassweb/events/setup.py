import events.models as emodels
from django.utils.translation import ugettext as _

def setup():
    # If some EventItems exist already we are not adding any more
    if not emodels.EventItem.objects.all().exists():
        event_item = emodels.EventItem(name="Diet",
                                       required=False,
                                       public=False,
                                       hide_in_print_view=False,
                                       type=emodels.EventItem.TYPE_STR,
                                       )
        event_item.save()
        event_item = emodels.EventItem(name="Association",
                                       required=False,
                                       public=True,
                                       hide_in_print_view=False,
                                       type=emodels.EventItem.TYPE_STR,
                                       )
        event_item.save()