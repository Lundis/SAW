from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from install.forms import AssociationForm, ModulesForm
from users.forms import LoginForm
from users.models import SAWPermission
from menu.logic import get_all_menu_items
from menu.models import Menu, MenuItem, MenuTemplate
from menu.forms import MenuForm
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
        MenuItem.remove_disabled_items()
        # create settings menu
        setup_settings()
        return HttpResponseRedirect('menu')

    context = {'form': form}
    return render(request, 'install/modules.html', context)


@has_permission(CAN_INSTALL)
def menu(request):

    main_menu, created = Menu.get_or_create("main_menu", MenuTemplate.default())
    login_menu, created = Menu.get_or_create("login_menu")
    if InstallProgress.is_menu_set():
        # fetch items from current menus
        menu_items = main_menu.items()
        login_items = login_menu.items()
        available_items = get_other_items(menu_items + login_items)
    else:
        # use default layout
        menu_items, login_items, available_items = get_all_menu_items()
    form = MenuForm(request.POST or None,
                    menus=(main_menu, login_menu),
                    initial_items={main_menu.menu_name: menu_items,
                                   login_menu.menu_name: login_items},
                    available_items=available_items)
    if form.is_valid():
        form.put_items_in_menus()
        InstallProgress.menu_set()
        return HttpResponseRedirect('finished')

    context = {'form': form}
    return render(request, 'install/menu.html', context)


def get_other_items(occupied=[]):
    menu_items, login_items, other_items = get_all_menu_items()
    all_items = menu_items + login_items + other_items
    return [item for item in all_items if not item in occupied]


@has_permission(CAN_INSTALL)
def finished(request):
    setup_default_groups()
    InstallProgress.finish()
    context = {}
    return render(request, 'install/finished.html', context)