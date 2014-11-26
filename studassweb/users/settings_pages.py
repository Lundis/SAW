from django.conf.urls import patterns, url
from .decorators import has_permission
from django.shortcuts import render
from .groups import group_names, get_permissions_in_group
from django.contrib.auth.models import Group
from .register import EDIT_LOGIN_SETTINGS, EDIT_PROFILE, EDIT_PERMISSIONS

urlpatterns = patterns('',
    url(r'^permissions/$', 'users.settings_pages.edit_permissions', name='users_settings_edit_permissions'),
    url(r'^user/$',        'users.settings_pages.edit_user',        name='users_settings_edit_user'),
    url(r'^login/$',       'users.settings_pages.edit_login',       name='users_settings_edit_login'),
)


@has_permission(EDIT_PERMISSIONS)
def edit_permissions(request):
    groups = Group.objects.filter(name__in=group_names)
    group_list = []
    for group in groups:
        group_list += [{'name': group,
                        'permissions': get_permissions_in_group(group)}]
    return render(request, "users/permission_settings.html", {'groups': group_list})


@has_permission(EDIT_PROFILE)
def edit_user(request):
    return render(request, "users/user_settings.html", {})


@has_permission(EDIT_LOGIN_SETTINGS)
def edit_login(request):
    return render(request, "users/login_settings.html", {})
