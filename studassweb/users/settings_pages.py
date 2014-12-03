from django.conf.urls import patterns, url
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .decorators import has_permission
from .groups import group_names, get_permissions_in_group
from .register import EDIT_LOGIN_SETTINGS, EDIT_PROFILE, EDIT_PERMISSIONS
from .forms import UserBaseForm, ProfileForm
from .models import UserExtension

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
    user = request.user
    user_ext = UserExtension.objects.get(user=user)

    user_form = UserBaseForm(request.POST or None, instance=user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=user_ext)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile_form.save()
        return HttpResponseRedirect(reverse("users_view_profile", username=user.username))
    context = {'user_form': user_form,
               'profile_form': profile_form}
    return render(request, "users/user_settings.html", context)


@has_permission(EDIT_LOGIN_SETTINGS)
def edit_login(request):
    return render(request, "users/login_settings.html", {})

