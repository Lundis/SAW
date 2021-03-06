# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from base.models import DisabledModule
from base.setup import setup_css_map
from install.forms import AssociationForm, ModulesForm
from users.forms import LoginForm
from menu.logic import get_all_menu_items
from menu.models import Menu
from menu.forms import MenuForm
from menu.setup import setup_menu_module
from .models import InstallProgress
from users.decorators import has_permission
from users.groups import setup_default_groups_and_permissions, put_user_in_standard_group, WEBMASTER
from .register import CAN_INSTALL
from base.models import SiteConfiguration
import logging

logger = logging.getLogger(__name__)


def welcome(request):
    setup_default_groups_and_permissions()
    setup_css_map()
    context = {}
    if not request.user.is_authenticated():
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            login_form.login_user(request)
        else:
            context['form'] = login_form
    else:
        if request.user.is_superuser:
            put_user_in_standard_group(request.user, WEBMASTER)

    return render(request, 'install/welcome.html', context)


@has_permission(CAN_INSTALL)
def association(request):
    form = AssociationForm(request.POST or None)
    if form.is_valid():
        form.apply()
        site_config = SiteConfiguration.instance()
        site_config.base_url = request.build_absolute_uri("/")[:-1]
        site_config.save()
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
        DisabledModule.execute_for_all_enabled("setup", "setup")
        return HttpResponseRedirect('menu')

    context = {'form': form}
    return render(request, 'install/modules.html', context)


@has_permission(CAN_INSTALL)
def menu(request):
    # set up menus
    setup_menu_module()
    main_menu = Menu.get("main_menu")
    login_menu = Menu.get("login_menu")
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


def get_other_items(occupied=()):
    menu_items, login_items, other_items = get_all_menu_items()
    all_items = menu_items + login_items + other_items
    return [item for item in all_items if item not in occupied]


@has_permission(CAN_INSTALL)
def finished(request):
    InstallProgress.finish()
    context = {}
    return render(request, 'install/finished.html', context)
