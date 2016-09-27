# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import FrontPageItem
from users.permissions import has_user_perm
from users.decorators import has_permission
from .register import CAN_EDIT_FRONTPAGE, CAN_VIEW_FRONTPAGE


@has_permission(CAN_VIEW_FRONTPAGE)
def frontpage(request, edit_mode=False):
    if edit_mode and not has_user_perm(request.user, CAN_EDIT_FRONTPAGE):
        return HttpResponseForbidden("You do not have permissions to edit the frontpage")

    context = {'edit_mode': edit_mode,
               'main_items': FrontPageItem.objects.filter(location=FrontPageItem.MAINBAR),
               'side_items': FrontPageItem.objects.filter(location=FrontPageItem.SIDEBAR),
               'loc_mainbar': FrontPageItem.MAINBAR,
               'loc_sidebar': FrontPageItem.SIDEBAR,
               'loc_hidden': FrontPageItem.HIDDEN}
    if edit_mode:
        context['hidden_items'] = FrontPageItem.objects.filter(location=FrontPageItem.HIDDEN)
    return render(request, 'frontpage/frontpage.html', context)
