from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from base.models import DisabledModule
from install.forms import AssociationForm, ModulesForm
from users.forms import LoginForm
from users.models import SAWPermission
from menu.logic import get_all_menu_items
from menu.models import Menu
from menu.forms import MenuForm
from menu.setup import setup_menu_module
from .models import InstallProgress
from users.decorators import has_permission
from users.groups import setup_default_groups_and_permissions, put_user_in_standard_group, WEBMASTER
from .register import CAN_INSTALL
import logging

logger = logging.getLogger(__name__)


def welcome(request):
    setup_default_groups_and_permissions()
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
    logger.info('In association, form is defined: %s', bool(form))
    if form.is_valid():
        form.apply()
        InstallProgress.site_name_set()
        logger.info('In association, redirecting to modules')
        return HttpResponseRedirect('modules')
    context = {'form': form}
    return render(request, 'install/assoc.html', context)


@has_permission(CAN_INSTALL)
def modules(request):
    form = ModulesForm(request.POST or None, modules=settings.OPTIONAL_APPS)
    logger.info('In modules, form is defined: %s', bool(form))
    if form.is_valid():
        form.apply()
        InstallProgress.modules_set()
        DisabledModule.execute_for_all_enabled("register", "setup")
        logger.info('In modules, redirecting to menu')
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
        logger.info('in Menu, is_menu_set() equals True')
        # fetch items from current menus
        menu_items = main_menu.items()
        login_items = login_menu.items()
        available_items = get_other_items(menu_items + login_items)
    else:
        logger.info('in Menu, is_menu_set() equals False')
        # use default layout
        menu_items, login_items, available_items = get_all_menu_items()
    form = MenuForm(request.POST or None,
                    menus=(main_menu, login_menu),
                    initial_items={main_menu.menu_name: menu_items,
                                   login_menu.menu_name: login_items},
                    available_items=available_items)
    if form.is_valid():
        logger.info('in Menu, form.is_valid() equals True')
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
    logger.info('in Finished')
    InstallProgress.finish()
    context = {}
    return render(request, 'install/finished.html', context)