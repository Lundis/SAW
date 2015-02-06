from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import FeedbackForm


def give_feedback(request):
    if request.POST:
        form = FeedbackForm(request.POST or None)
    if form.is_valid():
        form.save(request=request)
        return HttpResponse("Your feedback has been saved!")
    else:
        return HttpResponseNotAllowed(['POST'])
