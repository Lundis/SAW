# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import FrontPageItem
from users.permissions import has_user_perm
from users.decorators import has_permission
from .register import CAN_EDIT_FRONTPAGE, CAN_VIEW_FRONTPAGE
from base.models import DisabledModule


@has_permission(CAN_VIEW_FRONTPAGE)
def frontpage(request, edit_mode=False):
    if edit_mode and not has_user_perm(request.user, CAN_EDIT_FRONTPAGE):
        return HttpResponseForbidden("You do not have permissions to edit the frontpage")
    main_items = FrontPageItem.objects.filter(location=FrontPageItem.MAINBAR)
    side_items = FrontPageItem.objects.filter(location=FrontPageItem.SIDEBAR)
    hidden_items = FrontPageItem.objects.filter(location=FrontPageItem.HIDDEN)

    main_items = remove_items_from_disabled_modules(main_items)
    side_items = remove_items_from_disabled_modules(side_items)
    hidden_items = remove_items_from_disabled_modules(hidden_items)

    context = {
        'edit_mode': edit_mode,
        'main_items': main_items,
        'side_items': side_items,
        'loc_mainbar': FrontPageItem.MAINBAR,
        'loc_sidebar': FrontPageItem.SIDEBAR,
        'loc_hidden': FrontPageItem.HIDDEN
    }
    if edit_mode:
        context['hidden_items'] = hidden_items
    return render(request, 'frontpage/frontpage.html', context)


def remove_items_from_disabled_modules(items):
    """

    :param items:
    :return:
    """
    for item in items:
        if DisabledModule.is_disabled(item.module):
            items = items.exclude(pk=item.pk)
    return items
