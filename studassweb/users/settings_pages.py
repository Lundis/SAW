from django.conf.urls import patterns, url
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .decorators import has_permission
from .groups import group_names, get_permissions_in_group
from .register import EDIT_LOGIN_SETTINGS, EDIT_PROFILE, EDIT_PERMISSIONS
from .forms import UserBaseForm, ProfileForm, CustomGroupForm
from .models import UserExtension
from settings.sections import SECTION_PERSONAL_SETTINGS, SECTION_USERS, Section

urlpatterns = patterns('',
    url(r'^%s/permissions/$' % SECTION_USERS,
        'users.settings_pages.edit_permissions',
        name='users_settings_edit_permissions'),

    url(r'^%s/groups/$' % SECTION_USERS,
        'users.settings_pages.edit_groups',
        name='users_settings_edit_groups'),

    url(r'^%s/groups/(?P<group_id>\d+)$' % SECTION_USERS,
        'users.settings_pages.edit_groups',
        name='users_settings_edit_group'),

    url(r'^%s/groups/new$' % SECTION_USERS,
        'users.settings_pages.edit_groups',
        {'new': True},
        name='users_settings_new_group'),

    url(r'^%s/user/$' % SECTION_PERSONAL_SETTINGS,
        'users.settings_pages.edit_user',
        name='users_settings_edit_user'),

    url(r'^%s/login/$' % SECTION_USERS,
        'users.settings_pages.edit_login',
        name='users_settings_edit_login'),
)


@has_permission(EDIT_PERMISSIONS)
def edit_permissions(request):
    """
    A page for editing permissions in the default groups
    :param request:
    :return:
    """
    section = Section.get_section(SECTION_USERS)
    groups = Group.objects.filter(name__in=group_names)
    group_list = []
    for group in groups:
        group_list += [{'name': group,
                        'permissions': get_permissions_in_group(group)}]
    # TODO: mega permission form
    context = {'section': section,
               'groups': group_list}
    return render(request, "users/settings/permission_settings.html", context)


@has_permission(EDIT_PERMISSIONS)
def edit_groups(request, group_id=None, new=False):
    """
    A page for editing custom groups.
    :param request:
    :param group_id:
    :return:
    """
    can_edit = True
    if group_id is not None:
        try:
            group = Group.objects.get(id=group_id)
            # Don't allow editing of standard groups
            if group.name in group_names:
                can_edit = False
        except Group.DoesNotExist:
            raise Http404("Group with id %s not found" % group_id)
    else:
        group = None
    form = None
    if new or (group is not None and can_edit):
        form = CustomGroupForm(request.POST or None, instance=group)
        if form.is_valid():
            group = form.save()
            # Redirect to avoid refresh-related problems
            return HttpResponseRedirect(reverse("users_settings_edit_group",
                                                kwargs={'group_id': group.id}))

    custom_groups = Group.objects.exclude(name__in=group_names)
    section = Section.get_section(SECTION_USERS)
    context = {'section': section,
               'groups': custom_groups,
               'group': group,
               'form': form}
    return render(request, "users/settings/edit_groups.html", context)


@has_permission(EDIT_PROFILE)
def edit_user(request):
    section = Section.get_section(SECTION_PERSONAL_SETTINGS)
    user = request.user
    user_ext = UserExtension.objects.get(user=user)

    user_form = UserBaseForm(request.POST or None, instance=user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=user_ext)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile_form.save()
        return HttpResponseRedirect(reverse("users_view_profile", kwargs={"username": user.username}))
    context = {'user_form': user_form,
               'profile_form': profile_form,
               'section': section}
    return render(request, "users/settings/user_settings.html", context)


@has_permission(EDIT_LOGIN_SETTINGS)
def edit_login(request):
    section = Section.get_section(SECTION_USERS)
    context = {'section': section}
    return render(request, "users/settings/login_settings.html", context)

