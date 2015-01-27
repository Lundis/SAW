from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .sections import Section

@login_required()
def main(request):
    return render(request, "settings/base.html")


@login_required()
def view_sections(request):
    user = request.user
    sections = Section.get_all_sections()
    sections = [s for s in sections if s.can_view(user)]
    if len(sections) == 1:
        return HttpResponseRedirect(reverse("settings_view_section", args=(sections[0],)))
    context = {'sections': sections}
    return render(request, "settings/main.html", context)


@login_required()
def view_section(request, section):
    context = {'section': section}
    return render(request, "settings/view_section.html", context)