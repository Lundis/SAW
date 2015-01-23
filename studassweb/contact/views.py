from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from users import permissions
from .forms import MessageForm
from .models import Message
from .register import CAN_VIEW_CONTACT_INFO, CAN_USE_CONTACT_FORM, CAN_VIEW_MESSAGES
from django.core.urlresolvers import reverse
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


def home(request):
    if not permissions.has_user_perm(request.user, CAN_VIEW_CONTACT_INFO):
        logger.warning('User %s tried to view contact info', request.user)
        return HttpResponseForbidden('You don\'t have permission to view contact info!')

    return render(request, "contact/show_contact_info.html")


def write_message(request):
    if not permissions.has_user_perm(request.user, CAN_USE_CONTACT_FORM):
        logger.warning('User %s tried to write a message', request.user)
        return HttpResponseForbidden('You don\'t have permission to write message!')

    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            temp = form.save(commit=False)
            temp.from_person = request.user
            temp.save()
            messages.success(request,"Message succesfully sent!")
            return HttpResponseRedirect(reverse("contact_write_message"))

    context = {'form': form}

    return render(request, "contact/write_message.html", context)


def read_messages(request):
    if not permissions.has_user_perm(request.user, CAN_VIEW_MESSAGES):
        logger.warning('User %s tried to read messages', request.user)
        return HttpResponseForbidden('You don\'t have permission to read messages!')

    msgs = Message.objects.filter().order_by('-date_and_time')

    return render(request, "contact/view_messages.html",{'msgs': msgs,})