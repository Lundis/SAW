from django.http import HttpResponseNotAllowed
from django_ajax.decorators import ajax
from .forms import PlacementForm
from users.decorators import has_permission
from .register import CAN_EDIT_FRONTPAGE
import logging

logger = logging.getLogger(__name__)


@ajax
@has_permission(CAN_EDIT_FRONTPAGE)
def move_item(request):
    """
    POST variables: item_id, ordering_index, location
    ordering_index > 0
    location in (FrontPageItem.MAINBAR, FrontPageItem.SIDEBAR, FrontPageItem.HIDDEN)
    :param request:
    :return:
    """
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = PlacementForm(request.POST)
    if form.is_valid():
        form.save()
        logger.info("Moving item succeeded")
    else:
        logger.info("Moving item failed: " + form.errors)
