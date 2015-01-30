from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from users import permissions
from .forms import MessageForm
from .models import Message
from .register import CAN_VIEW_CONTACT_INFO, CAN_USE_CONTACT_FORM, CAN_VIEW_MESSAGES
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext
from base.models import SiteConfiguration
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

            try:
                send_mail(
                    ugettext("Site message from ")+" \"" + str(temp.from_person) +
                    "\" Title: " + form.cleaned_data['title'], form.cleaned_data['message'],
                    form.cleaned_data['from_email'], [SiteConfiguration.instance().association_contact_email])

            except BadHeaderError:
                messages.error(request, "Bad header, message not sent!")
                return HttpResponseRedirect(reverse("contact_write_message"))

            messages.success(request, "Message successfully sent!")
            return HttpResponseRedirect(reverse("contact_home"))

    context = {'form': form}

    return render(request, "contact/write_message.html", context)


def read_messages(request):
    if not permissions.has_user_perm(request.user, CAN_VIEW_MESSAGES):
        logger.warning('User %s tried to read messages', request.user)
        return HttpResponseForbidden('You don\'t have permission to read messages!')

    msgs = Message.objects.filter().order_by('-date_and_time')

    return render(request, "contact/view_messages.html",{'msgs': msgs,})


def delete_message(request, message_id):
    if request.method == 'POST':
        try:
            msg = Message.objects.get(id=message_id)
            if permissions.has_user_perm(request.user, CAN_VIEW_MESSAGES):
                title = msg.title
                msg.delete()
                messages.success(request, "Message \""+title+"\" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("contact_read_messages"))
            else:
                logger.warning('User %s tried to delete message %s', request.user, message_id)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except Message.DoesNotExist:
            return HttpResponseNotFound('No such message!')
    else:
            logger.warning('Attempted to access delete_message via GET')
            return HttpResponseNotAllowed(['POST', ])