from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.conf import settings
from install.forms import AssociationForm, ModulesForm, MenuForm
from users.forms import LoginForm
from menu.logic import get_all_menu_items
from menu.models import Menu, MenuItem


def first_letter_to_upper(str):
    """
    :param str:
    :return: str with the first letter in upper case
    """
    return str[0].upper() + str[1:]

# make an array of arrays, where each entry represents [stage_name, user_friendly_name]
stages = [[s, _(first_letter_to_upper(s))] for s in ["welcome", "association", "modules", "menu", "finished"]]

def welcome(request):
    context = {'stages': stages,
               'current_stage_index': 0,
               'current_stage': stages[0]}
    if not request.user.is_authenticated():
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            login_form.login_user(request)
        else:
            context['form'] = login_form


    return render(request, 'install/welcome.html', context)

@login_required
def association(request):
    form = AssociationForm(request.POST or None)
    if form.is_valid():
        form.apply()
        return HttpResponseRedirect('modules')
    context = {'form': form,
               'stages': stages,
               'current_stage_index': 1,
               'current_stage': stages[1]}
    return render(request, 'install/assoc.html', context)

@login_required
def modules(request):
    form = ModulesForm(request.POST or None, modules=settings.OPTIONAL_APPS)
    if form.is_valid():
        form.apply()
        return HttpResponseRedirect('menu')

    context = {'form': form,
               'stages': stages,
               'current_stage_index': 2,
               'current_stage': stages[2]}
    return render(request, 'install/modules.html', context)

@login_required
def menu(request):
    form = MenuForm(request.POST or None)
    if form.is_valid():
        form.apply()
        return HttpResponseRedirect('finished')

    available_items = get_all_menu_items()

    menu_items = get_main_menu_items()
    #filter away menu items
    available_items = [item for item in available_items if item not in menu_items]

    login_items = get_login_menu_items()
    # filter away login items
    available_items = [item for item in available_items if item not in login_items]

    context = {'menu_items': menu_items,
               'login_items': login_items,
               'available_items': available_items,
               'form': form,
               'stages': stages,
               'current_stage_index': 3,
               'current_stage': stages[3]}
    return render(request, 'install/menu.html', context)

def get_main_menu_items():
    """
    :return: a list of menu items that represents either the current main menu or the default main menu
    """
    main_menu = Menu.get_or_none("main_menu")
    if main_menu:
        # load the current menu items
        return main_menu.items()
    else:
        # load default menu items for the main menu
        print("main defaults: ", MenuItem.get_defaults(MenuItem.MAIN_MENU))
        return MenuItem.get_defaults(MenuItem.MAIN_MENU)

def get_login_menu_items():
    """
    :return: a list of menu items that represents either the curren login menu or the default login menu
    """
    login_menu = Menu.get_or_none("login_menu")
    if login_menu:
        # load the current menu items
        return login_menu.items()
    else:
        # load default menu items for the login menu
        print("login defaults: ", MenuItem.get_defaults(MenuItem.LOGIN_MENU))
        return MenuItem.get_defaults(MenuItem.LOGIN_MENU)

@login_required
def finished(request):
    context = {'stages': stages,
               'current_stage_index': 4,
               'current_stage': stages[4]}
    return render(request, 'install/finished.html', context)