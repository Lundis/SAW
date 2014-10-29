from django.shortcuts import render
from login.forms import LoginForm
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

def login_view(request):
    """
    Renders a login form.

    If it is a form submission request, then redirect to whatever page GET['next'] points to.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login_user(request)
            next = request.GET.get('next', None)
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                # go to the front page if nothing is specified
                return HttpResponseRedirect("/")
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})