from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',                              'gallery.views.view_gallery',   name='gallery_main'),
    url(r'^album/(?P<id>\d+)$',             'gallery.views.view_album',     name='gallery_view_album'),
    url(r'^album/(?P<id>\d+)/edit$',        'gallery.views.edit_album',     name='gallery_edit_album'),
    url(r'^album/create$',                  'gallery.views.create_album',   name='gallery_create_album'),
    url(r'^picture/(?P<id>\d+)$',           'gallery.views.view_picture',   name='gallery_view_picture'),
    url(r'^picture/(?P<id>\d+)/edit$',      'gallery.views.view_picture',   name='gallery_view_picture'),
)
