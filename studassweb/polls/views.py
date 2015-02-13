from django.shortcuts import render
from polls.models import *
from django.http import HttpResponseNotFound
from polls.forms import *
from users import permissions
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from .register import CAN_CREATE_POLLS, CAN_DELETE_ALL_POLLS
from django.forms.models import inlineformset_factory
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)


def home(request):
    all_polls = Poll.objects.filter().order_by('-publication')
    return render(request, "polls/view_main.html",
                  {'all_polls': all_polls},)


def view_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
        choices = Choice.objects.filter(id_to_poll=poll_id)

        if poll.can_user_vote(request):
            if poll.can_vote_on_many:
                pass

            else:
                form = ChoiceFormSingle(request.POST or None, poll_choices=choices)

            if form.is_valid():
                form.save(request)
                form = None

        else:
            form = None

        context = {'form': form, 'poll': poll, 'choices': choices}
        return render(request, 'polls/view_poll.html', context)
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

    context = {'form': form, 'choicesformset': choiceformset}
    return render(request, 'polls/add_edit_poll.html', context)


def delete_poll(request, poll_id):
    if request.method == 'POST':
        try:
            poll = Poll.objects.get(id=poll_id)
            if permissions.has_user_perm(request.user, CAN_DELETE_ALL_POLLS) or poll.created_by == request.user:
                name = str(poll)

                poll.delete()
                messages.success(request, "Poll "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("polls_home"))
            else:
                logger.warning('User %s tried to delete exam %s', request.user, poll_id)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except Poll.DoesNotExist:
            return HttpResponseNotFound('No such poll!')
    else:
        logger.warning('Attempted to access delete_poll via GET')
        return HttpResponseNotAllowed(['POST', ])


def edit_poll(request, poll_id):
    if not permissions.has_user_perm(request.user, CAN_CREATE_POLLS):
        logger.warning('User %s tried to add poll', request.user)
        return HttpResponseForbidden('You don\'t have permission to add polls!')
    poll = Poll.objects.get(id=poll_id)
    form = PollForm(instance=poll)
    choices_factory = inlineformset_factory(Poll, Choice, fields=('id', 'name',), extra=1, can_delete=True)
    choiceformset = choices_factory(instance=poll, prefix='dynamix')

    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        choiceformset = choices_factory(request.POST, request.FILES, instance=poll, prefix='dynamix')
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

    context = {'form': form, 'choicesformset': choiceformset}
    return render(request, 'polls/add_edit_poll.html', context)





