from django.shortcuts import render
from gallery.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse

def view_gallery(request):
    return render(request, 'gallery/view_gallery.html')


def view_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        print (album)
        return render(request, 'gallery/view_album.html', {
            'album': album},)
    except Album.DoesNotExist:
        return HttpResponseNotFound('error')


def edit_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        return render(request, 'gallery/edit_album.html', {
            'album': album},)
    except Album.DoesNotExist:
        return HttpResponseNotFound('error')


def create_album(request, album_id=None):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:

        album = None

    form = AlbumForm(instance=album)

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            tmp = form.save()
            return HttpResponseRedirect(reverse('gallery_view_album', kwargs={'album_id': tmp.id}))

    context = {'form': form}
    return render(request, 'gallery/create_album.html', context)



def view_picture(request, album_id):
    """
    Renders the picture with the specified id
    :param request:
    :return:
    """
    pass

def edit_picture(request, album_id):
    """
    Lets user edit picture
    :param request:
    :return:
    """
    pass