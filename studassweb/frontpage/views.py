from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import FrontPageItem


def frontpage(request, edit_mode=False):
    context = {'edit_mode': edit_mode,
               'main_items': FrontPageItem.objects.filter(location=FrontPageItem.MAINBAR),
               'side_items': FrontPageItem.objects.filter(location=FrontPageItem.SIDEBAR)}
    if edit_mode:
        context['hidden_items'] = FrontPageItem.objects.filter(location=FrontPageItem.HIDDEN)
    return render(request, 'frontpage/frontpage.html', context)