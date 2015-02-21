from django.conf.urls import patterns, url
from users.decorators import has_permission
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from .models import Menu, MenuItem, TYPE_USER
from .register import EDIT_MENUS
from .forms import MenuForm, MenuCreationForm, MenuItemForm, MainMenuForm
from .models import MainMenuSettings
from base.views import delete_confirmation_view
from settings.sections import SECTION_MENU, SECTION_APPEARANCE, Section


urlpatterns = patterns('',
                       url(r'^%s/select_menu$' % SECTION_MENU,
                           'menu.settings_pages.select_menu',
                           name='menu_settings_select_menu'),

                       url(r'^%s/edit_menu_item/(?P<item_id>\d+)$' % SECTION_MENU,
                           'menu.settings_pages.edit_menu_item',
                           name='menu_settings_edit_menu_item'),

                       url(r'^%s/new_menu_item$' % SECTION_MENU,
                           'menu.settings_pages.edit_menu_item',
                           name='menu_settings_new_menu_item'),

                       url(r'^%s/delete_menu_item/(?P<item_id>\d+)$' % SECTION_MENU,
                           'menu.settings_pages.delete_menu_item',
                           name='menu_settings_delete_menu_item'),

                       url(r'^%s/new_menu$' % SECTION_MENU,
                           'menu.settings_pages.new_menu',
                           name='menu_settings_new_menu'),

                       url(r'^%s/delete_menu/(?P<menu_id>\d+)$' % SECTION_MENU,
                           'menu.settings_pages.delete_menu',
                           name='menu_settings_delete_menu'),

                       url(r'^%s/edit_menu/(?P<menu_id>\d+)$' % SECTION_MENU,
                           'menu.settings_pages.edit_menu',
                           name='menu_settings_edit_menu'),

                       url(r'^%s/edit_menu_layout$' % SECTION_APPEARANCE,
                           'menu.settings_pages.edit_menu_layout',
                           name='menu_settings_edit_menu_layout')
)

menu_section = Section.get_section(SECTION_MENU)


@has_permission(EDIT_MENUS)
def select_menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, "menu/settings/select_menu.html", {'menus': Menu.objects.all(),
                                                              'menu_items': menu_items,
                                                              'section': menu_section})


@has_permission(EDIT_MENUS)
def new_menu(request):
    form = MenuCreationForm(request.POST or None)
    if form.is_valid():
        menu = form.save()
        return HttpResponseRedirect(reverse("menu_settings_edit_menu", kwargs={'menu_id': menu.id}))
    context = {'form': form,
               'section': menu_section}
    return render(request, "menu/settings/new_menu.html", context)


@has_permission(EDIT_MENUS)
def delete_menu(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        raise Http404

    if menu.created_by != TYPE_USER:
        return HttpResponseBadRequest("Only user-managed menus can be deleted")

    return delete_confirmation_view(request,
                                    menu,
                                    reverse("menu_settings_delete_menu", kwargs={'menu_id': menu.id}),
                                    reverse('menu_settings_select_menu'))


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
        return HttpResponseRedirect(reverse("menu_settings_select_menu"))
    context = {'menu': menu,
               'form': form,
               'section': menu_section}
    return render(request, "menu/settings/edit_menu.html", context)


@has_permission(EDIT_MENUS)
def edit_menu_item(request, item_id=None):
    menu_item = None
    try:
        menu_item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        pass
    if menu_item and menu_item.created_by != TYPE_USER:
        return HttpResponseBadRequest("Only user-managed menu items can be edited")

    form = MenuItemForm(request.POST or None,
                        instance=menu_item)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("menu_settings_select_menu"))
    context = {'menu_item': menu_item,
               'form': form,
               'section': menu_section}
    return render(request, "menu/settings/edit_menu_item.html", context)


@has_permission(EDIT_MENUS)
def delete_menu_item(request, item_id):
    try:
        menu_item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        raise Http404

    if menu_item.created_by != TYPE_USER:
        return HttpResponseBadRequest("Only user-managed menu items can be deleted")

    return delete_confirmation_view(request,
                                    menu_item,
                                    reverse("menu_settings_delete_menu", kwargs={'item_id': menu_item.id}),
                                    reverse('menu_settings_select_menu'))


@has_permission(EDIT_MENUS)
def edit_menu_layout(request):
    form = MainMenuForm(request.POST or None,
                        request.FILES or None,
                        instance=MainMenuSettings.instance())
    if form.is_valid():
        form.save()
    section = Section.get_section(SECTION_APPEARANCE)
    context = {'form': form,
               'section': section}
    return render(request, 'menu/settings/edit_menu_layout.html', context)