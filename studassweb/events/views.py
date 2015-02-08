from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseServerError
from .models import Event, EventSignup, EventItem
from django.http import HttpResponseRedirect
from users import permissions
from .register import CAN_VIEW_EVENTS, CAN_CREATE_EVENTS, CAN_SIGNUP_FOR_EVENTS, CAN_VIEW_SIGNUP_INFO
from .forms import EventForm, EventSignupForm, EventItemsForm, SignupItemsForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext as _
from base.utils import generate_email_ver_code
from django.conf import settings
from base.models import SiteConfiguration
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
import sys
import logging

logger = logging.getLogger(__name__)

MAIN_PREFIX = "mainevent"
ITEMS_PREFIX = "eventitems"


def home(request):
    events = Event.objects.filter().order_by('start')
    return render(request, 'events/view_events.html', {'events':events})


# TODO we shouldn't have all this code in the view
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        signupform = EventSignupForm(request.POST or None, prefix=MAIN_PREFIX)
        signupitemsform = SignupItemsForm(request.POST or None, event=event, prefix=ITEMS_PREFIX)
        if signupform.is_valid() and signupitemsform.is_valid():
            temp = signupform.save(commit=False)
            temp.event = event
            temp.delete_confirmation_code = generate_email_ver_code()
            while EventSignup.objects.filter(delete_confirmation_code=temp.delete_confirmation_code).exists():
                temp.delete_confirmation_code = generate_email_ver_code()
            if not request.user.is_anonymous():
                temp.user = request.user

            # We need to save to db here to get id, but we should remove it if we couldn't send email
            temp.save()
            signupitemsform.save(event=event)

            try:
                from_email = settings.NO_REPLY_EMAIL
                to_emails = [temp.email]
                title = _("{0}: You are now signed up to {1}").format(
                    SiteConfiguration.instance().association_name,
                    event.title
                )
                logger.info("Sending event email from %s to %s" % (from_email, to_emails[0]))
                send_mail(
                    title,
                    _("You are now registered to event {0}."
                      " If you want to cancel you registration you can do so here: {1} before the deadline, {2}").
                    format(
                        event.title,

                        request.scheme +
                        "://" +
                        request.get_host() +
                        reverse("events_delete_event_signup_by_code", args=[temp.delete_confirmation_code]),

                        event.signup_deadline
                    ),
                    from_email,
                    to_emails)

            except BadHeaderError:
                logger.error("BadHeaderError sending email to {0}".format(to_emails))
                temp.delete()
                messages.error(request, _("BadHeaderError, newlines in email adress?"))
                return HttpResponseRedirect(reverse("events_view_event", args=str(event.id)))
            except:
                logger.error("Exception {0} sending email to {1}".format(sys.exc_info()[0], to_emails))
                temp.delete()
                messages.error(request, _("Error, please try again"))
                return HttpResponseRedirect(reverse("events_view_event", args=str(event.id)))

            # Remove form after signing up
            signupform = None

            messages.success(request, _("Successfully signed up to event!"))

        signups = EventSignup.objects.filter(event=event)

        return render(request, 'events/event.html', {
            'event': event, 'signupform': signupform, 'signupitemsform': signupitemsform, 'signups': signups})
    except Event.DoesNotExist:
        logger.warning('Could not find event with id %s', event_id)
        return HttpResponseNotFound('No event with that id found')


def add_event(request):

    if not permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
        logger.warning('User %s tried to add event', request.user)
        return HttpResponseForbidden('You don\'t have permission to add events!')
    form = EventForm(prefix=MAIN_PREFIX)
    form_items = EventItemsForm(prefix=ITEMS_PREFIX)

    if request.method == 'POST':
        form = EventForm(request.POST, prefix=MAIN_PREFIX)
        form_items = EventItemsForm(request.POST, prefix=ITEMS_PREFIX)
        if form.is_valid() and form_items.is_valid():
            temp = form.save(commit=False)
            temp.author = request.user
            temp.save()

            form_items.save(temp)
            return HttpResponseRedirect(reverse("events_view_event", args=[form.instance.id]))

    context = {'form': form, 'form_items': form_items}
    return render(request, 'events/add_edit_event.html', context)


def edit_event(request, event_id):
    if not permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
            logger.warning('User %s tried to edit event %s', request.user, event_id)
            return HttpResponseForbidden('You don\'t have permission to edit this event!')
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        logger.warning('User %s tried to edit nonexistant event id %s', request.user, event_id)
        return HttpResponseNotFound('No such role!')

    form = EventForm(instance=event, prefix=MAIN_PREFIX)
    form_items = EventItemsForm(event=event, prefix=ITEMS_PREFIX)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event, prefix=MAIN_PREFIX)
        form_items = EventItemsForm(request.POST, prefix=ITEMS_PREFIX, event=event)
        if form.is_valid() and form_items.is_valid:
            tmp_event = form.save()
            form_items.save(tmp_event)
            return HttpResponseRedirect(reverse("events_view_event", args=[form.instance.id]))

    context = {'form': form, 'form_items': form_items}
    return render(request, 'events/add_edit_event.html', context)


def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            if permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
                name = str(event)
                event.delete()
                messages.success(request, "Event "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("events_home"))
            else:
                logger.warning('User %s tried to delete event %s', request.user, event)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except Event.DoesNotExist:
            logger.warning('User %s tried to delete nonexistant event id %s', request.user, event_id)
            return HttpResponseNotFound('No such event!')
    else:
            logger.warning('Attempted to access delete_event via other method than POST')
            return HttpResponseNotAllowed(['POST', ])


def delete_event_signup(request, event_signup_id):
    try:
        signup = EventSignup.objects.get(id=event_signup_id)

    except EventSignup.DoesNotExist:
        logger.warning('User %s tried to delete nonexistant signup id %s', request.user, event_signup_id)
        return HttpResponseNotFound(_('No such EventSignup!'))

    if request.method == 'POST':
        if not permissions.has_user_perm(request.user, CAN_VIEW_SIGNUP_INFO):

            logger.warning('User %s tried to delete signup id %s', request.user, event_signup_id)
            return HttpResponseForbidden(_('You don\'t have permission to remove this!'))

    else:
            logger.warning('Attempted to access delete_event_signup via other method than POST')
            return HttpResponseNotAllowed(['POST', ])

    # Checks completed, let's remove this!
    signup_name = str(signup.name)
    event = signup.event
    signup.delete()
    messages.success(
        request,
        _("Event signup for {0} from event {1} was successfully removed!").format(signup_name, event.title)
    )
    return HttpResponseRedirect(reverse("events_view_event", args=str(event.id)))


# This view is used when deleting a view using delete_confirmation_code
class DeleteEventSignupByCodeView(DeleteView):
    model = EventSignup

    def get_object(self, *args, **kwargs):
        try:
            return EventSignup.objects.get(delete_confirmation_code=self.kwargs['delete_confirmation_code'])

        except EventSignup.DoesNotExist:
            logger.error("Wrong event delete_confirmation_code {0}".format(self.kwargs['delete_confirmation_code']))
            messages.error(
                self.request,
                _("Could not unregister from event, maybe you are already unregistered?")
            )
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return HttpResponseRedirect(reverse("events_home"))
        return super(DeleteView, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return HttpResponseRedirect(reverse("events_home"))

        event = self.object.event
        signup_name = self.object.name
        self.object.delete()
        messages.success(
            request,
            _("Event signup for {0} from event {1} was successfully removed!").format(signup_name, event.title)
        )
        return HttpResponseRedirect(reverse("events_view_event", args=str(event.id)))


class AddEventItemView(CreateView):
    model = EventItem
    fields = ['name']
    success_url = reverse_lazy("events_list_eventitems")

    def dispatch(self, request, *args, **kwargs):
        if permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
            return super(AddEventItemView, self).dispatch(request, *args, **kwargs)
        messages.error(request, _("You don't have permission to add event items"))
        return HttpResponseRedirect(reverse("events_home"))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        messages.success(self.request, _("Succesfully added event item"))
        return super(AddEventItemView, self).form_valid(form)


class EditEventItemView(UpdateView):
    model = EventItem
    fields = ['name']
    success_url = reverse_lazy("events_list_eventitems")

    def dispatch(self, request, *args, **kwargs):
        if permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
            return super(EditEventItemView, self).dispatch(request, *args, **kwargs)
        messages.error(request, _("You don't have permission to edit event items"))
        return HttpResponseRedirect(reverse("events_home"))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        messages.success(self.request, _("Succesfully updated event item"))
        return super(EditEventItemView, self).form_valid(form)


class DeleteEventItemView(DeleteView):
    model = EventItem
    success_url = reverse_lazy("events_list_eventitems")

    def dispatch(self, request, *args, **kwargs):
        if permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
            return super(DeleteEventItemView, self).dispatch(request, *args, **kwargs)
        messages.error(request, _("You don't have permission to add event items"))
        return HttpResponseRedirect(reverse("events_home"))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        messages.success(self.request, _("Succesfully removed event item"))
        return super(DeleteEventItemView, self).form_valid(form)


class ListEventItemsView(ListView):
    model = EventItem

    def dispatch(self, request, *args, **kwargs):
        if permissions.has_user_perm(request.user, CAN_CREATE_EVENTS):
            return super(ListEventItemsView, self).dispatch(request, *args, **kwargs)
        messages.error(request, _("You don't have permission to list event items"))
        return HttpResponseRedirect(reverse("events_home"))
