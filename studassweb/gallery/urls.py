from django.conf.urls import url, include
from . import views

slug_pattern = '(?P<slug>[-\w\d]+)'

urlpatterns = [
    url(r'^$',                                    views.view_gallery,     name='gallery_main'),
    url(r'^album/%s/$' % slug_pattern,            views.view_album,       name='gallery_view_album'),
    url(r'^create_album/$',                       views.add_edit_album,   name='gallery_create_album'),
    url(r'^edit_album/%s/$' % slug_pattern,       views.add_edit_album,   name='gallery_edit_album'),
    url(r'^delete_album/%s/$' % slug_pattern,     views.delete_album,     name='gallery_delete_album'),
    url(r'^manage_album/%s/$' % slug_pattern,     views.manage_album,     name='gallery_manage_album'),
    url(r'^delete_picture/(?P<photo_id>\d+)$',    views.delete_picture,   name='gallery_delete_picture'),
    url(r'^your_uploads/', include('multiuploader.urls'))
]
