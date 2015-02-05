from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from install.models import InstallProgress


def frontpage(request):
    if not InstallProgress.is_finished():
        return HttpResponseRedirect(reverse("install_welcome"))
    return render(request, 'frontpage/frontpage.html')