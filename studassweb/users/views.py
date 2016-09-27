# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseServerError
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.mail import send_mail, BadHeaderError
from members.models import Member
from .forms import LoginForm, RegisterForm
from .models import UserExtension
from .groups import put_user_in_standard_group, LOGGED_ON
from base.models import SiteConfiguration
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    """
    Renders a login form.

    If it is a form submission request, then redirect to whatever page GET['next'] points to.
    :param request:
    :return:
    """
    form = LoginForm(request.POST or None)
    if form.is_valid():
        form.login_user(request)
        next = request.GET.get('next', None)
        if next is not None:
            return HttpResponseRedirect(next)
        else:
            # go to the front page if nothing is specified
            return HttpResponseRedirect("/")
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')


def register(request):
    """
    Renders a register form.
    :param request:
    :return:
    """
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user_ext = form.save()
        put_user_in_standard_group(user_ext.user, LOGGED_ON)
        user = authenticate(username=form.cleaned_data['user_name'],
                            password=form.cleaned_data['password'])
        login(request, user)
        return HttpResponseRedirect(reverse("users_register_thanks"))

    context = {'form': form}
    return render(request, 'users/register/register.html', context)


@login_required
def register_thanks(request):
    try:
        user_ext = UserExtension.objects.get(user=request.user)
    except UserExtension.DoesNotExist:
        raise Http404
    context = {}

    from_email = settings.NO_REPLY_EMAIL
    to_emails = [request.user.email]
    try:
        title = _("Confirmation email from ") + SiteConfiguration.instance().association_name
        logger.info("sending verification email from %s to %s" % (from_email, to_emails[0]))
        send_mail(
            title,
            _("Hello! Please visit this link: ") +
            request.scheme + "://" + request.get_host() +
            reverse("users_verify_email", kwargs={'code': user_ext.email_verification_code, }) +
            _(" to confirm your email."),
            from_email,
            to_emails)

    except BadHeaderError:
        logger.info("BadHeaderError when sending verification email from %s to %s" % (from_email, to_emails[0]))
        return HttpResponseServerError("BadHeaderError, newlines in email adress?")
    return render(request, 'users/register/register_thanks.html', context)


def view_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    try:
        user_ext = UserExtension.objects.get(user=user)
    except UserExtension.DoesNotExist:
        user_ext = UserExtension.create_for_user(user)

    try:
        member = Member.objects.get(user_ext=user_ext)
    except Member.DoesNotExist:
        member = None
    context = {'user_ext': user_ext,
               'member': member}
    return render(request, 'users/view_profile.html', context)


def verify_email(request, code):
    if code is None:
        return HttpResponseBadRequest("The verification code is missing")
    if len(code) != 32:
        return HttpResponseBadRequest("The verification code has an invalid length")
    success = UserExtension.verify_email(code)
    return render(request, 'users/register/email_verification.html', {'success': success})
