from django.conf.urls import patterns, url
from .decorators import has_permission
from django.shortcuts import render
from .groups import group_names, get_permissions_in_group
from django.contrib.auth.models import Group

urlpatterns = patterns('',
    url(r'^permissions/$', 'users.settings_pages.edit_permissions', name='edit permissions'),
    url(r'^user/$', 'users.settings_pages.edit_user', name='edit user'),
    url(r'^login/$', 'users.settings_pages.edit_login', name='edit login'),
)

@has_permission("can_edit_permissions")
def edit_permissions(request):
    groups = Group.objects.filter(name__in=group_names)
    group_list = []
    for group in groups:
        group_list += [{'name': group,
                        'permissions': get_permissions_in_group(group)}]
    return render(request, "users/permission_settings.html", {'groups': group_list})

@has_permission("can_edit_profile")
def edit_user(request):
    return render(request, "users/user_settings.html", {})

@has_permission("can_edit_login_settings")
def edit_login(request):
    return render(request, "users/login_settings.html", {})
