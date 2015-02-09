from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from base.models import DisabledModule
from install.models import InstallProgress


class VerifyModuleEnabled:

    def process_request(self, request):
        # The first item in the path is the module name, such as /settings/blabla
        module = request.path[1:].split("/")[0]
        # The frontpage is a special case
        if module == "":
            module = "frontpage"

        if not InstallProgress.is_finished() and module != "install" and module != "admin":
            return HttpResponseRedirect(reverse("install_welcome"))
        if DisabledModule.is_disabled(module):
            return HttpResponseNotFound("The requested module is disabled")
