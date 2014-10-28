from django.shortcuts import render

def home(request):
    """
    Renders the albums in the order defined by a GET variable
    :param request:
    :return:
    """
    pass

def view_album(request, id):
    """
    Renders the pictures in the album with the specified id in the order defined by a GET variable
    :param request:
    :return:
    """
    pass

def edit_album(request, id):
    """
    Renders the album edit blabla
    :param request:
    :return:
    """
    pass

def create_album(request):
    """
    Renders the album form and verifies the form on submit
    :param request:
    :return:
    """
    pass

def view_picture(request, id):
    """
    Renders the picture with the specified id
    :param request:
    :return:
    """
    pass

def edit_picture(request, id):
    """
    Lets user edit picture
    :param request:
    :return:
    """
    pass