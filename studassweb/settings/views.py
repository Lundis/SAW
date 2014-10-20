from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def main(request):
    # TODO: get all settings from all modules
    return render(request, "settings/base.html")