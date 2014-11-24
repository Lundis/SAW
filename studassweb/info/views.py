from django.shortcuts import render
from users.decorators import has_permission
from .models import InfoCategory, InfoPage
from .forms import InfoPageForm, InfoCategoryForm
from django.http import Http404, HttpResponseRedirect

@has_permission("can_view_public_info_pages")
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


@has_permission("can_view_public_info_pages")
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


@has_permission("can_edit_info_pages")
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


@has_permission("can_view_public_info_pages")
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


@has_permission("can_edit_info_pages")
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
         return render(request, "info/edit_category.html", {'category': category,
                                                            'form': form})