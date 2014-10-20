from django.shortcuts import render

@login_required()
def main(request):
    return "settings page!"