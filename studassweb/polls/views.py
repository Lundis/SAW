from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from django.forms.models import inlineformset_factory
from django.contrib import messages
from users.decorators import has_permission
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse

from .register import CAN_CREATE_POLLS
from .models import Poll, Choice
from .forms import PollForm, ChoiceFormMultiple, ChoiceFormSingle

import logging


logger = logging.getLogger(__name__)


def home(request):
    all_polls = Poll.objects.filter().order_by('-publication')
    return render(request, "polls/view_main.html",
                  {'all_polls': all_polls},)


def view_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponseNotFound('No poll with that id found')

    if not poll.can_view(request.user):
        return HttpResponseForbidden("You do not have access to view this poll")
    choices = Choice.objects.filter(id_to_poll=poll_id)

    if poll.can_user_vote(request):
        if poll.can_vote_on_many:
            form = ChoiceFormMultiple(request.POST or None, poll_choices=choices, poll=poll)

        else:
            form = ChoiceFormSingle(request.POST or None, poll_choices=choices, poll=poll)

        if form.is_valid():
            form.save(request)
            form = None

    else:
        form = None

    context = {'form': form, 'poll': poll, 'choices': choices}
    return render(request, 'polls/view_poll.html', context)


@has_permission(CAN_CREATE_POLLS)
def add_poll(request):
    form = PollForm(request.POST or None)
    choices_factory = inlineformset_factory(Poll, Choice, fields=('id', 'name',), extra=1, can_delete=True)
    choiceformset = choices_factory(request.POST or None, prefix='dynamix')

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
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponseNotFound('No such poll!')

    if not poll.can_edit(request.user):
        raise SuspiciousOperation("User tried to delete poll without access")

    if request.method == 'POST':
        name = str(poll)

        poll.delete()
        messages.success(request, "Poll " + name + " was successfully deleted!")
        return HttpResponseRedirect(reverse("polls_home"))
    else:
        logger.warning('Attempted to access delete_poll via GET')
        return HttpResponseNotAllowed(['POST', ])


def edit_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if not poll.can_edit(request.user):
        raise SuspiciousOperation("User tried to edit poll without access")

    form = PollForm(request.POST or None, instance=poll)
    choices_factory = inlineformset_factory(Poll, Choice, fields=('id', 'name',), extra=0, can_delete=True)
    choiceformset = choices_factory(request.POST or None, instance=poll, prefix='dynamix')

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





