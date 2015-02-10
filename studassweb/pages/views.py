from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from users.decorators import has_permission
from users.permissions import has_user_perm
from .models import InfoCategory, InfoPage, InfoPageEdit
from .forms import InfoPageForm, InfoCategoryForm
from .register import EDIT, VIEW_PUBLIC
from base.views import delete_confirmation_view



@has_permission(VIEW_PUBLIC)
def main(request):
    """
    renders a list of the different categories. This page shouldn't be used in general, or just for searching purposes.
    :param request:
    :return:
    """
    categories = InfoCategory.objects.all()
    pages_without_parent = InfoPage.objects.filter(category=None, for_frontpage=False)
    if has_user_perm(request.user, EDIT):
        frontpage_pages = InfoPage.objects.filter(for_frontpage=True)
    else:
        frontpage_pages = None
    return render(request, 'info/main.html', {'categories': categories,
                                              'orphans': pages_without_parent,
                                              'frontpage_pages': frontpage_pages})


@has_permission(VIEW_PUBLIC)
def view_page(request, page_id, revision_id=None):
    """
    view a page
    :param request:
    :return:
    """
    page = InfoPage.objects.get(id=page_id)
    category = page.category
    revisions = page.revisions()
    if revision_id is None:
        current_revision = page.revisions().first()
    else:
        try:
            current_revision = revisions.get(id=revision_id)
        except InfoPageEdit.DoesNotExist:
            raise Http404(_("The requested revision could not be found"))
    return render(request, 'info/view_page.html', {'category': category,
                                                   'page': page,
                                                   'current_revision': current_revision})


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

    form = InfoPageForm(request.POST or None,
                        instance=page,
                        initial={'category': category},
                        user=request.user)
    if form.is_valid():
        new_page = form.save()
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
def delete_category(request, category_id):
    try:
        category = InfoCategory.objects.get(id=category_id)
    except InfoCategory.DoesNotExist:
        raise Http404(_("The requested object could not be found"))
    return delete_confirmation_view(request,
                                    item=category,
                                    form_url=reverse("pages_delete_category",
                                                     kwargs={'category_id': category_id}),
                                    redirect_url=reverse('pages_view_categories'))


@has_permission(EDIT)
def delete_page(request, page_id):
    try:
        category = InfoPage.objects.get(id=page_id)
    except InfoPage.DoesNotExist:
        raise Http404(_("The requested object could not be found"))
    return delete_confirmation_view(request,
                                    item=category,
                                    form_url=reverse("pages_delete_page",
                                                     kwargs={'page_id': page_id}),
                                    redirect_url=reverse('pages_view_categories'))