from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from install.forms import AssociationForm

@login_required
def welcome(request):
    context = {'current_url': request.get_full_path(),
               'current': 'welcome'}
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
               'current': 'association',
               'form': form,}
    return render(request, 'install/base.html', context)

@login_required
def modules(request):

    context = {'previous': 'association',
               'current': 'modules'}
    return render(request, 'install/base.html', context)

@login_required
def menu(request):
    context = {'previous': 'modules',
               'current': 'menu'}
    return render(request, 'install/base.html', context)

@login_required
def finished(request):
    context = {'previous': 'menu',
               'current': 'finished'}
    return render(request, 'install/base.html', context)