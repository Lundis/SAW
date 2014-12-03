from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from members.models import Member
from .forms import LoginForm, RegisterForm
from .models import UserExtension
from .groups import put_user_in_default_group, LOGGED_ON


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
        put_user_in_default_group(user_ext.user, LOGGED_ON)
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
    context = {'code': user_ext.email_verification_code}

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
        member = Member.objects.get(user=user)
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
