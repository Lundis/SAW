from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from users.decorators import has_permission
from menu.models import MenuItem, Menu
from .models import InfoCategory, InfoPage
from .forms import InfoPageForm, InfoCategoryForm
from .register import EDIT, VIEW_PUBLIC


@has_permission(VIEW_PUBLIC)
def main(request):
    """
    renders a list of the different categories. This page shouldn't be used in general, or just for searching purposes.
    :param request:
    :return:
    """
    categories = InfoCategory.objects.all()
    pages_without_parent = InfoPage.objects.filter(category=None)
    return render(request, "info/main.html", {'categories': categories,
                                              'pages': pages_without_parent})


@has_permission(VIEW_PUBLIC)
def view_page(request, category_id, page_id):
    """
    view a page
    :param request:
    :return:
    """
    category = InfoCategory.objects.get(id=category_id)
    page = InfoPage.objects.get(id=page_id)
    return render(request, "info/view_page.html", {'category': category,
                                                   'page': page})


@has_permission(EDIT)
def edit_page(request, category_id, page_id=None):
    """
    edit or create a page
    :param request:
    :return:
    """
    category = None
    try:
        category = InfoCategory.objects.get(id=category_id)
    except InfoCategory.DoesNotExist:
        raise Http404
    page = None

    try:
        page = InfoPage.objects.get(id=page_id)
    except InfoPage.DoesNotExist:
        pass

    form = InfoPageForm(request.POST or None, instance=page)
    if form.is_valid():
        page = form.save()
        page.category = category
        page.save()
        return HttpResponseRedirect(page.get_absolute_url())
    else:
        return render(request, "info/edit_page.html", {'category': category,
                                                       'form': form})


@has_permission(VIEW_PUBLIC)
def view_category(request, category_id):
    """
    renders a list of the pages in the specified category
    :param request:
    :return:
    """
    try:
        category = InfoCategory.objects.get(id=category_id)
    except InfoCategory.DoesNotExist:
        raise Http404

    return render(request, "info/view_category.html", {'category': category})


@has_permission(EDIT)
def edit_category(request, category_id=None):
    """
    edit or create a new category
    :param request:
    :return:
    """

    category = None
    try:
        category = InfoCategory.objects.get(id=category_id)
    except InfoCategory.DoesNotExist:
        pass

    form = InfoCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        cat = form.save()
        # if it's a new category
        if not category:
            # add it to the info menu
            #TODO: set the same permission as the category
            item = MenuItem.get_or_create("info", cat.name, cat.get_absolute_url(), permission=None)
            menu, created = Menu.objects.get_or_create(menu_name="info_top_menu")
            #TODO: menu item index
            menu.add_item(item, 0)
        return HttpResponseRedirect(cat.get_absolute_url())
    else:
         return render(request, "info/edit_category.html", {'category': category,
                                                            'form': form})