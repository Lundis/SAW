from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect,\
    HttpResponseNotAllowed, HttpResponseServerError, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext as _
from users import permissions
from users.decorators import has_permission
from .forms import MessageForm
from .models import Message, ContactInfo
from .register import CAN_VIEW_CONTACT_INFO, CAN_USE_CONTACT_FORM, CAN_VIEW_MESSAGES
import logging

logger = logging.getLogger(__name__)


@has_permission(CAN_VIEW_CONTACT_INFO)
def home(request):
    contacts = ContactInfo.objects.all()
    context = {'contacts': contacts}
    return render(request, "contact/show_contact_info.html", context)


@has_permission(CAN_USE_CONTACT_FORM)
def write_message(request, contact_id):
    try:
        contact = ContactInfo.objects.get(id=contact_id)
    except ContactInfo.DoesNotExist:
        raise Http404("No such contact exists")

    if not (contact.save_to_db or contact.send_email):
        logger.warning('Messages in contact module are neither saved to db nor sent as email.'
                       'It is thus not functional')
        return HttpResponseServerError(
            'Messages in contact module are neither saved to db nor sent as email.'
            'It is thus not functional'
        )
    form = MessageForm(request.POST or None, user=request.user)
    if form.is_valid():
        if contact.save_to_db:
            form.save(contact=contact, from_person=request.user)

        if contact.send_email:
            try:
                send_mail(
                    _("Site message from ")+" \"" + str(request.user) +
                    "\" Title: " + form.cleaned_data['title'], form.cleaned_data['message'],
                    form.cleaned_data['from_email'],
                    [contact.email])

            except BadHeaderError:
                # TODO: use a message that the user can understand
                messages.error(request, "Bad header, message not sent!")
                return HttpResponseRedirect(reverse("contact_write_message"))

        messages.success(request, "Message successfully sent!")
        return HttpResponseRedirect(reverse("contact_home"))

    context = {'form': form,
               'contact': contact}

    return render(request, "contact/write_message.html", context)


@has_permission(CAN_VIEW_MESSAGES)
def read_messages(request, contact_id):
    try:
        contact = ContactInfo.objects.get(id=contact_id)
    except ContactInfo.DoesNotExist:
        raise Http404("The Specified contact was not found")

    msgs = Message.objects.filter(contact=contact).order_by('-date_and_time')
    context = {'msgs': msgs,
               'contact': contact}
    return render(request, "contact/view_messages.html", context)


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