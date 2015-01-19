from django.shortcuts import render
from polls.models import *
from django.http import HttpResponseNotFound
from polls.forms import *
from users import permissions
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from .register import CAN_CREATE_POLLS
import logging


logger = logging.getLogger(__name__)

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


def add_poll(request):
    if not permissions.has_user_perm(request.user, CAN_CREATE_POLLS):
        logger.warning('User %s tried to add poll', request.user)
        return HttpResponseForbidden('You don\'t have permission to add polls!')
    form = PollForm()

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_role", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'polls/add_edit_poll.html', context)

def remove_poll(request,poll_id):
    pass

def edit_poll(request,poll_id):
    pass




def set_user_choice(request, choice_id=-1):
    try:
        choice = Poll.objects.get(id=choice_id)
    except Choice.DoesNotExist:
        choice = None

    form = ChoiceForm(instance=choice)

    context = {'form': form}
    return render(request, 'polls/pollchoices.html', context)


