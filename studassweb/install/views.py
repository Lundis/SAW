from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.conf import settings
from install.forms import AssociationForm, ModulesForm, MenuForm
from login.forms import LoginForm


def first_letter_to_upper(str):
    """
    :param str:
    :return: str with the first letter in upper case
    """
    return str[0].upper() + str[1:]

# make an array of arrays, where each entry represents [stage_name, user_friendly_name]
stages = [[s, _(first_letter_to_upper(s))] for s in ["welcome", "association", "modules", "menu", "finished"]]

def welcome(request):
    context = {'current_url': request.get_full_path(),

               'stages': stages,
               'current_stage_index': 0,
               'current_stage': stages[0]}
    if not request.user.is_authenticated():
        login_form = LoginForm(request or None)
        if login_form.is_valid():
            return HttpResponseRedirect('modules')


    return render(request, 'install/base.html', context)

@login_required
def association(request):
    form = AssociationForm(request.POST or None)
    if form.is_valid():
        #TODO: Save to database
        return HttpResponseRedirect('modules')

    context = {'previous': 'welcome',
               'form': form,
               'stages': stages,
               'current_stage_index': 1,
               'current_stage': stages[1]}
    return render(request, 'install/base.html', context)

@login_required
def modules(request):
    form = ModulesForm(request.POST or None, modules=settings.OPTIONAL_APPS)
    if form.is_valid():
        #TODO: save to database
        return HttpResponseRedirect('menu')

    context = {'previous': 'association',
               'form': form,
               'stages': stages,
               'current_stage_index': 2,
               'current_stage': stages[2]}
    return render(request, 'install/base.html', context)

@login_required
def menu(request):
    form = MenuForm(request.POST or None)
    if form.is_valid():
        #TODO: save to database
        return HttpResponseRedirect('finished')
    # TODO: get all available menu items and let the user choose which he wants, and in which order.
    context = {'previous': 'modules',
               'form': form,
               'stages': stages,
               'current_stage_index': 3,
               'current_stage': stages[3]}
    return render(request, 'install/base.html', context)

@login_required
def finished(request):
    context = {'previous': 'menu',
               'stages': stages,
               'current_stage_index': 4,
               'current_stage': stages[4]}
    return render(request, 'install/base.html', context)