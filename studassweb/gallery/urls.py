from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'gallery.views.view_gallery', name='view_gallery'),
    url(r'^album/(?P<id>\d+)$', 'gallery.views.view_album', name='view_album'),
    url(r'^album/(?P<id>\d+)/edit$', 'gallery.views.edit_album', name='edit_album'),
    url(r'^album/create$', 'gallery.views.create_album', name='create_album'),
    url(r'^picture/(?P<id>\d+)$', 'gallery.views.view_picture', name='view_picture'),
    url(r'^picture/(?P<id>\d+)/edit$', 'gallery.views.view_picture', name='view_picture'),
)
