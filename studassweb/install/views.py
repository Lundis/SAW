from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from install.forms import AssociationForm, ModulesForm, MenuForm
from users.forms import LoginForm
from users.models import SAWPermission
from menu.logic import get_all_menu_items
from menu.models import Menu, MenuItem
from .models import InstallProgress
from users.decorators import has_permission
from users.groups import setup_default_groups
from settings.setup import setup_settings
from .register import CAN_INSTALL


def welcome(request):
    # create the can_install permission if it doesn't exist
    SAWPermission.get_or_create("can_install", "Allows you to use the installation wizard")
    context = {}
    if not request.user.is_authenticated():
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            login_form.login_user(request)
        else:
            context['form'] = login_form

    return render(request, 'install/welcome.html', context)


@has_permission(CAN_INSTALL)
def association(request):
    form = AssociationForm(request.POST or None)
    if form.is_valid():
        form.apply()
        InstallProgress.site_name_set()
        return HttpResponseRedirect('modules')
    context = {'form': form}
    return render(request, 'install/assoc.html', context)


@has_permission(CAN_INSTALL)
def modules(request):
    form = ModulesForm(request.POST or None, modules=settings.OPTIONAL_APPS)
    if form.is_valid():
        form.apply()
        InstallProgress.modules_set()
        # create settings menu
        setup_settings()
        return HttpResponseRedirect('menu')

    context = {'form': form}
    return render(request, 'install/modules.html', context)


@has_permission(CAN_INSTALL)
def menu(request):
    form = MenuForm(request.POST or None)
    if form.is_valid():
        form.apply()
        InstallProgress.menu_set()
        return HttpResponseRedirect('finished')

    menu_items, login_items, other_items = get_all_menu_items()

    context = {'menu_items': menu_items,
               'login_items': login_items,
               'available_items': other_items,
               'form': form}
    return render(request, 'install/menu.html', context)


@has_permission(CAN_INSTALL)
def finished(request):
    setup_default_groups()
    InstallProgress.finish()
    context = {}
    return render(request, 'install/finished.html', context)