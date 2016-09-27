# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .sections import Section


@login_required()
def view_sections(request):
    user = request.user
    sections = Section.get_all_sections()
    sections = [s for s in sections if s.can_view(user)]
    if len(sections) == 1:
        return HttpResponseRedirect(sections[0].get_absolute_url())
    context = {'sections': sections}
    return render(request, "settings/main.html", context)


@login_required()
def view_section(request, section_id):
    section = Section.get_section(section_id)
    if len(section.pages) == 1:
        return HttpResponseRedirect(section.pages[0].get_absolute_url())
    context = {'section': section}
    return render(request, "settings/view_section.html", context)
