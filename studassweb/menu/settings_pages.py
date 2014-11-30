from django.conf.urls import patterns, url
from users.decorators import has_permission
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Menu, MenuItem
from .register import EDIT_MENUS
from .forms import MenuForm


urlpatterns = patterns('',
    url(r'^$', 'menu.settings_pages.select_menu', name='menu_settings_select_menu'),
    url(r'^edit/(?P<menu_id>\d+)/$', 'menu.settings_pages.edit_menu', name='menu_settings_edit_menu'),
)


@has_permission(EDIT_MENUS)
def select_menu(request):
    return render(request, "menu/settings_select_menu.html", {'menus': Menu.objects.all()})


@has_permission(EDIT_MENUS)
def edit_menu(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        raise Http404

    # Get all available menu items
    available_items = MenuItem.objects.all()
    # Filter away the ones in the menu
    available_items = [item for item in available_items if not menu.contains(item)]

    form = MenuForm(request.POST or None,
                    menus=(menu,),
                    available_items=available_items)
    if form.is_valid():
        form.put_items_in_menus()
    context = {'menu': menu,
               'form': form}
    return render(request, "menu/settings_edit_menu.html", context)
