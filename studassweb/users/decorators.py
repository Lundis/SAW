from .permissions import has_user_perm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

# http://stackoverflow.com/questions/9030255/django-add-optional-arguments-to-decorator
def has_permission(permission):
    """
    Much magic here
    :param permission: The permission as a string
    """

    def _method_wrapper(view_method):

        def _arguments_wrapper(request, *args, **kwargs):
            if has_user_perm(request.user, permission):
                return view_method(request, *args, **kwargs)
            elif not request.user.is_authenticated():
                return HttpResponseRedirect("/users/login/&next=" + request.path)
            else:
                raise PermissionDenied

        return _arguments_wrapper

    return _method_wrapper