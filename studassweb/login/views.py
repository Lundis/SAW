from django.shortcuts import render

def login(request):
    """
    Renders a login form.

    If it is a form submission request, then redirect to whatever page GET['next'] points to.
    :param request:
    :return:
    """
    pass