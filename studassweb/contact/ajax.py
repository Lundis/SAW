from django_ajax.decorators import ajax
from django.http import HttpResponseNotAllowed
from users.decorators import has_permission
from .register import CAN_VIEW_MESSAGES
from .forms import MarkAsHandledForm


@ajax
@has_permission(CAN_VIEW_MESSAGES)
def mark_message_as_handled(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    else:
        form = MarkAsHandledForm(request.POST)
        if form.is_valid():
            form.save()