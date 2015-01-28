from django.shortcuts import render
from polls.models import *
from django.http import HttpResponseNotFound
from polls.forms import *
from users import permissions
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from .register import CAN_CREATE_POLLS
from django.forms.models import inlineformset_factory
import logging


logger = logging.getLogger(__name__)

def home(request):
    all_polls = Poll.objects.filter().order_by('-publication')
    return render(request, "polls/view_main.html",
                {'all_polls':all_polls},)


def view_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
        choices = Choice.objects.filter(id_to_poll=poll_id)

        return render(request, 'polls/view_poll.html', {
            'poll': poll,'choices':choices},)
    except Poll.DoesNotExist:
        return HttpResponseNotFound('No poll with that id found')


def add_poll(request):
    if not permissions.has_user_perm(request.user, CAN_CREATE_POLLS):
        logger.warning('User %s tried to add poll', request.user)
        return HttpResponseForbidden('You don\'t have permission to add polls!')
    form = PollForm()
    choices_factory = inlineformset_factory(Poll, Choice, fields=('id', 'name',), extra=1, can_delete=True)
    choiceformset = choices_factory(prefix='dynamix')


    if request.method == 'POST':
        form = PollForm(request.POST)
        choiceformset = choices_factory(request.POST, request.FILES, prefix='dynamix')
        if form.is_valid() and choiceformset.is_valid():
            tmppoll = form.save(commit=False)
            tmppoll.created_by = request.user
            tmppoll.save()

            for obj in choiceformset.save(commit=False):
                obj.id_to_poll = tmppoll
                obj.save()

            for obj in choiceformset.deleted_objects:
                obj.delete()

            return HttpResponseRedirect(reverse("polls_view_poll", args=[tmppoll.id]))

    context = {'form': form,'choicesformset':choiceformset}
    return render(request, 'polls/add_edit_poll.html', context)

def remove_poll(request,poll_id):
    pass

def edit_poll(request,poll_id):
    if not permissions.has_user_perm(request.user, CAN_CREATE_POLLS):
        logger.warning('User %s tried to add poll', request.user)
        return HttpResponseForbidden('You don\'t have permission to add polls!')
    poll = Poll.objects.get(id=poll_id)
    form = PollForm(instance=poll)
    choices_factory = inlineformset_factory(Poll, Choice, fields=('id', 'name',), extra=1, can_delete=True)
    choiceformset = choices_factory(instance=poll,prefix='dynamix')


    if request.method == 'POST':
        form = PollForm(request.POST,instance=poll)
        choiceformset = choices_factory(request.POST, request.FILES,instance=poll, prefix='dynamix')
        if form.is_valid() and choiceformset.is_valid():
            tmppoll = form.save(commit=False)
            tmppoll.created_by = request.user
            tmppoll.save()

            for obj in choiceformset.save(commit=False):
                obj.id_to_poll = tmppoll
                obj.save()

            for obj in choiceformset.deleted_objects:
                obj.delete()

            return HttpResponseRedirect(reverse("polls_view_poll", args=[tmppoll.id]))

    context = {'form': form,'choicesformset':choiceformset}
    return render(request, 'polls/add_edit_poll.html',context)


def remove_choice(request,choice_id):
    pass




def set_user_choice(request, choice_id=-1):
   pass


