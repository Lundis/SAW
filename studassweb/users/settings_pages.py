from django.conf.urls import patterns, url
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from settings.sections import SECTION_PERSONAL_SETTINGS, SECTION_USERS, Section
from base.forms import DummyForm
from .decorators import has_permission
from .groups import group_names
from .register import EDIT_LOGIN_SETTINGS, EDIT_PROFILE, EDIT_PERMISSIONS
from .forms import UserBaseForm, ProfileForm, CustomGroupForm, PermissionEditorForm
from .models import UserExtension, SAWPermission


urlpatterns = patterns('',
    url(r'^%s/permissions/$' % SECTION_USERS,
        'users.settings_pages.edit_permissions',
        name='users_settings_edit_permissions'),

    url(r'^%s/permissions/reset' % SECTION_USERS,
        'users.settings_pages.reset_permissions',
        name='users_settings_reset_permissions'),

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


def get_modules_with_permissions():
    perms_in_dicts = SAWPermission.objects.values("module").distinct()
    perms = [entry['module'] for entry in perms_in_dicts]
    return sorted(perms)


@has_permission(EDIT_PERMISSIONS)
def edit_permissions(request):
    """
    A page for editing permissions in the default groups
    :param request:
    :return:
    """
    section = Section.get_section(SECTION_USERS)
    groups = Group.objects.filter(name__in=group_names)
    group_dict = {}
    initial_items = {}
    orphans = {}
    for group in groups:
        group_dict[group.name] = group
        initial_items[group.name] = ()

    sawps = SAWPermission.objects.all()
    # Add each permission to its group
    for sawp in sawps:
        g = sawp.standard_group()
        if g is None:
            orphans += sawp,
        else:
            initial_items[g] += sawp,

    form = PermissionEditorForm(request.POST or None,
                                container_model=Group,
                                child_model=SAWPermission,
                                initial_items=initial_items,
                                available_items=orphans,
                                containers=group_dict,
                                all_items=sawps)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("users_settings_edit_permissions"))

    context = {'section': section,
               'groups': groups,
               'modules': get_modules_with_permissions(),
               'form': form}
    return render(request, "users/settings/permission_editor.html", context)


@has_permission(EDIT_PERMISSIONS)
def reset_permissions(request):
    if request.POST is not None:
        csrf_form = DummyForm(request.POST)
        if csrf_form.is_valid():
            sawps = SAWPermission.objects.all()
            for sawp in sawps:
                sawp.reset_to_default_group()
            return HttpResponseRedirect(reverse("users_settings_edit_permissions"))
    else:
        return HttpResponseNotAllowed(['POST'])


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
               'form': form,
               'modules': get_modules_with_permissions()}
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

