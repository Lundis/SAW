from django.conf.urls import patterns, url
from users.decorators import has_permission
from django.shortcuts import render
from django.contrib.auth.models import Group

urlpatterns = patterns('',
    url(r'^$', 'menu', name='menu_settings_edit_menu'),
)

@has_permission("can_edit_menu")
def edit_menu(request):
    return render(request, "users/menu_settings.html", {})
