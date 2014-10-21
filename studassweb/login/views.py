from django.shortcuts import render
from login.forms import LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
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
            # https://docs.djangoproject.com/en/1.7/topics/auth/default/#auth-web-requests
            user = authenticate(username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next = request.GET.get('next', None)
                    if next is not None:
                        return HttpResponseRedirect(next)
                    else:
                        # go to the front page if nothing is specified
                        return HttpResponseRedirect("/")
                else:
                    form.add_error(None, _("Your account has been disabled"))
            else:
                form.add_error(None, _("Wrong username and/or password"))
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})