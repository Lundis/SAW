from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseServerError
from .models import Event, EventSignup, EventItem, ItemInSignup
from django.http import HttpResponseRedirect, Http404
from users import permissions
from .register import CAN_VIEW_EVENTS, CAN_CREATE_EVENTS, CAN_SIGNUP_FOR_EVENTS, CAN_VIEW_SIGNUP_INFO
from .forms import EventForm, EventSignupForm, EventItemsForm, SignupItemsForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.conf import settings
from base.models import SiteConfiguration
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.template.loader import get_template
from django.template import Context
import sys
import logging

logger = logging.getLogger(__name__)

MAIN_PREFIX = "mainevent"
ITEMS_PREFIX = "eventitems"


def home(request):
    events = Event.objects.filter().order_by('start')
    return render(request, 'events/view_events.html', {'events':events})


# TODO we shouldn't have all this code in the view
# A lot of these errors should simply invalidate the form so the user can correct it!
def view_event(request, event_id=None, slug=None, signup_id=None, auth_code=None):
    try:
        if slug:
            event = Event.objects.get(slug=slug)
        elif event_id:
            event = Event.objects.get(id=event_id)
        else:
            logger.error('view_event was called without slug or event_id! This should never happen!')
            messages.error(request, _("Error in url!? This should never happen."))
            return HttpResponseRedirect(reverse("events_home"))
    except Event.DoesNotExist:
        logger.warning('Could not find event with slug %s or id %s', slug, event_id)
        return HttpResponseNotFound('Event not found')

    db_event_signup = None
    if auth_code:
        try:
            db_event_signup = EventSignup.objects.get(auth_code=auth_code)
        except EventSignup.DoesNotExist:
            raise Http404(_("Invalid auth code!"))
    elif signup_id:
        try:
            db_event_signup = EventSignup.objects.get(id=signup_id)
            if not db_event_signup.user_can_edit(request.user):
                logger.warning('Unauthorized user %s tried to edit signup id %s', request.user, signup_id)
                messages.error(request, _("You don't have permission to change this!"))
                return HttpResponseRedirect(event.get_absolute_url())
        except EventSignup.DoesNotExist:
            logger.warning('Could not find signup_id %s', request.user, signup_id)
            messages.error(request, _("Wrong signup id!"))
            return HttpResponseRedirect(event.get_absolute_url())

    initial_user_data = {}
    if request.user.is_authenticated() and not db_event_signup:
        initial_user_data = {'name': request.user.get_full_name(), 'email': request.user.email}

    signupform = EventSignupForm(request.POST or None, initial=initial_user_data, instance=db_event_signup, prefix=MAIN_PREFIX)
    signupitemsform = SignupItemsForm(request.POST or None, event=event, signup=db_event_signup, prefix=ITEMS_PREFIX)

    if signupform.is_valid() and signupitemsform.is_valid():
        temp_signup = signupform.save(user=request.user, event=event)
        try:
            signupitemsform.save(signup=temp_signup)
        except Exception as e:
            logger.error("Failed to save signup items!? (%s)", e)
            temp_signup.delete()

        from_email = settings.NO_REPLY_EMAIL
        to_emails = [temp_signup.email]
        title = _("{0}: You are now signed up to {1}").format(
            SiteConfiguration.instance().association_name,
            event.title
        )
        context = Context({'request': request,
                           'event': event,
                           'signup': temp_signup,
                           'signup_edit_url':
                               request.build_absolute_uri(reverse("events_view_event_edit_signup_by_code",
                                                                  kwargs={'event_id': event.id,
                                                                          'auth_code': temp_signup.auth_code})),
                           'signup_cancel_url':
                               request.build_absolute_uri(reverse("events_delete_event_signup_by_code",
                                                                  kwargs={'auth_code': temp_signup.auth_code}))})

        template = get_template("events/email.html")
        message = template.render(context)
        logger.info("Sending event email from %s to %s" % (from_email, to_emails[0]))
        try:
            send_mail(
                title,
                message,
                from_email,
                to_emails)
            return HttpResponseRedirect(reverse("events_view_event", kwargs={'slug': event.slug}))

        except BadHeaderError:
            logger.error("BadHeaderError sending email to {0}".format(to_emails))
            temp_signup.delete()
            messages.error(request, _("BadHeaderError, newlines in email adress?"))
            return HttpResponseRedirect(event.get_absolute_url())
        except:
            logger.error("Exception {0} sending email to {1}".format(sys.exc_info()[0], to_emails))
            temp_signup.delete()
            messages.error(request, _("Error, please try again"))
            return HttpResponseRedirect(event.get_absolute_url())

        messages.success(request, _("Successfully signed up to event!"))

    signups = EventSignup.objects.filter(event=event)

    return render(request, 'events/event.html', {
        'event': event, 'signupform': signupform, 'signupitemsform': signupitemsform, 'signups': signups})



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
            return HttpResponseRedirect(form.instance.get_absolute_url())

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
            return HttpResponseRedirect(form.instance.get_absolute_url())

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
        if not signup.user_can_edit(request.user):

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
    return HttpResponseRedirect(event.get_absolute_url())


# This view is used when deleting a view using auth_code
class DeleteEventSignupByCodeView(DeleteView):
    model = EventSignup

    def get_object(self, *args, **kwargs):
        try:
            return EventSignup.objects.get(auth_code=self.kwargs['auth_code'])

        except EventSignup.DoesNotExist:
            logger.error("Wrong event auth_code {0}".format(self.kwargs['auth_code']))
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
        return HttpResponseRedirect(event.get_absolute_url())


class AddEventItemView(CreateView):
    model = EventItem
    fields = ['name', 'type', 'required']
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
    fields = ['name', 'type', 'required']
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
