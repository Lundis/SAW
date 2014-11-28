from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


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