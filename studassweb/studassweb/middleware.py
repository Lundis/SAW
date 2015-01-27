from django.http import HttpResponseNotFound
from base.models import DisabledModule


class VerifyModuleEnabled:

    def process_request(self, request):
        # The first item in the path is the module name, such as /settings/blabla
        module = request.path[1:].split("/")[0]
        # The frontpage is a special case
        if module == "":
            module = "frontpage"
        if DisabledModule.is_disabled(module):
            return HttpResponseNotFound("The requested module is disabled")