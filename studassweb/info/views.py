from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from users.decorators import has_permission
from menu.models import MenuItem, Menu
from .models import InfoCategory, InfoPage
from .forms import InfoPageForm, InfoCategoryForm
from .register import EDIT, VIEW_PUBLIC
from base.forms import ConfirmationForm
from django.core.urlresolvers import reverse


@has_permission(VIEW_PUBLIC)
def main(request):
    """
    renders a list of the different categories. This page shouldn't be used in general, or just for searching purposes.
    :param request:
    :return:
    """
    categories = InfoCategory.objects.all()
    pages_without_parent = InfoPage.objects.filter(category=None)
    return render(request, 'info/main.html', {'categories': categories,
                                              'pages': pages_without_parent})


@has_permission(VIEW_PUBLIC)
def view_page(request, page_id):
    """
    view a page
    :param request:
    :return:
    """
    page = InfoPage.objects.get(id=page_id)
    category = page.category
    return render(request, 'info/view_page.html', {'category': category,
                                                   'page': page})


@has_permission(EDIT)
def edit_page(request, category_id=None, page_id=None):
    """
    edit or create a page
    :param request:
    :return:
    """
    page = None
    category = None
    try:
        page = InfoPage.objects.get(id=page_id)
        category = page.category
    except InfoPage.DoesNotExist:
        pass

    # if this is a new page and a category is specified
    if not category and category_id:
        try:
            category = InfoCategory.objects.get(id=category_id)
        except InfoCategory.DoesNotExist:
            pass

    form = InfoPageForm(request.POST or None, instance=page, initial={'category': category})
    if form.is_valid():
        new_page = form.save()
        new_page.category = category
        new_page.save()
        return HttpResponseRedirect(new_page.get_absolute_url())
    else:
        return render(request, 'info/edit_page.html', {'category': category,
                                                       'page': page,
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

    return render(request, 'info/view_category.html', {'category': category})


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
        return HttpResponseRedirect(cat.get_absolute_url())
    else:
        return render(request, 'info/edit_category.html', {'category': category,
                                                           'form': form})


@has_permission(EDIT)
def delete(request, category_id=None, page_id=None):
    if category_id and page_id:
        raise ValueError('You cannot delete both a category and a page at once')
    elif not category_id and not page_id:
        raise ValueError('You must specify a category or page to delete')

    category = None
    try:
        category = InfoCategory.objects.get(id=category_id)
    except InfoCategory.DoesNotExist:
        pass
    page = None
    try:
        page = InfoPage.objects.get(id=page_id)
    except InfoPage.DoesNotExist:
        pass

    form = ConfirmationForm(request.POST or None)
    if form.is_valid():
        if page:
            cat = page.category
            page.delete()
            if cat:
                return HttpResponseRedirect(cat.get_absolute_url())
        else:
            category.delete()
            return HttpResponseRedirect(reverse('info_view_categories'))


    return render(request, "info/delete.html", {'category': category,
                                                'page': page,
                                                'form': form})