# coding=utf-8
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django_ajax.decorators import ajax
from users.decorators import has_permission
from .forms import FeedbackForm
from .register import CAN_GIVE_FEEDBACK
from .models import Feedback
import logging

logger = logging.getLogger(__name__)


@ajax
@has_permission(CAN_GIVE_FEEDBACK)
def give_feedback(request):
    """

    :param request:
    :return:
    """
    if request.POST:
        form = FeedbackForm(request.POST or None, request=request, type=Feedback.FEEDBACK_HELPTEXT)
        if form.is_valid():
            form.save()
        else:
            logger.warn("Feedback form validation failed: %s" % form.errors)
            return HttpResponseBadRequest("Validation failed")
    else:
        return HttpResponseNotAllowed(['POST'])
