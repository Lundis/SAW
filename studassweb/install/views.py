from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from install.forms import AssociationForm


def first_letter_to_upper(str):
    """
    :param str:
    :return: str with the first letter in upper case
    """
    return str[0].upper() + str[1:]

stages = [[s, _(first_letter_to_upper(s))] for s in ["welcome", "association", "modules", "menu", "finished"]]

@login_required
def welcome(request):
    #TODO: put a login form here
    context = {'current_url': request.get_full_path(),
               'stages': stages,
               'current_stage_index': 0,
               'current_stage': stages[0]}
    return render(request, 'install/base.html', context)

@login_required
def association(request):
    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            #TODO: Save to database
            return HttpResponseRedirect('modules')
    else:
        # create a new form
        form = AssociationForm()


    context = {'previous': 'welcome',
               'form': form,
               'stages': stages,
               'current_stage_index': 1,
               'current_stage': stages[1]}
    return render(request, 'install/base.html', context)

@login_required
def modules(request):
    #TODO: get all available modules and list them and let the user choose which he wants
    context = {'previous': 'association',
               'stages': stages,
               'current_stage_index': 2,
               'current_stage': stages[2]}
    return render(request, 'install/base.html', context)

@login_required
def menu(request):
    # TODO: get all available menu items and let the user choose which he wants, and in which order.
    context = {'previous': 'modules',
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