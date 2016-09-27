# coding=utf-8
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse
from .groups import put_user_in_standard_group
from .register import EDIT_PERMISSIONS
from .decorators import has_permission


@has_permission(EDIT_PERMISSIONS)
def set_default_group(request, username, group_name):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User %s doesn't exist" % username)
    try:
        put_user_in_standard_group(user, group_name)
        return HttpResponse("OK")
    except ValueError:
        return HttpResponseBadRequest("Group %s is not one of the default groups" % group_name)
