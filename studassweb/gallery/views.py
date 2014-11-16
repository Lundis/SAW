from django.shortcuts import render
from gallery.forms import *

def view_gallery(request):
    return render(request, 'gallery/view_gallery.html')


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

def create_album(request, id=-1):
    form = AlbumForm

    context = {'form': form}
    return render(request, 'gallery/create_album.html', context)



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