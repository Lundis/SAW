from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .forms import LoginForm, RegisterForm
from .models import UserExtension


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
        form.save()
        return render(request, 'users/register.html')
    return render(request, 'users/register.html', {'form': form})


def view_profile(request, username):
    user = User.objects.get(username=username)
    user_ext = UserExtension.objects.get(user=user)
    context = {'user_ext': user_ext}
    return render(request, 'users/view_profile.html', context)