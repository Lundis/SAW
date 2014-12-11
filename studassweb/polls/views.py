from django.shortcuts import render
from polls.models import *
from django.http import HttpResponseNotFound
from polls.forms import *

def home(request):
    all_polls = Poll.objects.filter().order_by('-publication')
    return render(request, "polls/base.html",
                {'all_polls':all_polls},)


def view_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)

        return render(request, 'polls/view_poll.html', {
            'poll': poll},)
    except Poll.DoesNotExist:
        return HttpResponseNotFound('No poll with that id found')








def set_user_choice(request, choice_id=-1):
    try:
        choice = Poll.objects.get(id=choice_id)
    except Choice.DoesNotExist:
        choice = None

    form = ChoiceForm(instance=choice)

    context = {'form': form}
    return render(request, 'polls/pollchoices.html', context)


