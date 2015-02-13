from django.http import HttpResponseNotAllowed
from django_ajax.decorators import ajax
from .forms import PlacementForm


@ajax
def move_item(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = PlacementForm(request.POST)
    if form.is_valid():
        form.save()