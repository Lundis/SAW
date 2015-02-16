from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',                                    'gallery.views.view_gallery',     name='gallery_main'),
    url(r'^album/(?P<album_id>\d+)$',             'gallery.views.view_album',       name='gallery_view_album'),
    url(r'^picture/(?P<photo_id>\d+)$',           'gallery.views.view_picture',     name='gallery_view_picture'),
    url(r'^create_album/$',                       'gallery.views.add_edit_album',   name='gallery_create_album'),
    url(r'^add_picture/$',                        'gallery.views.add_edit_picture', name='gallery_add_picture'),
    url(r'^edit_album/(?P<album_id>\d+)$',        'gallery.views.add_edit_album',   name='gallery_edit_album'),
    url(r'^edit_picture/(?P<photo_id>\d+)$',      'gallery.views.add_edit_picture', name='gallery_edit_picture'),
    url(r'^delete_album/(?P<album_id>\d+)$',      'gallery.views.delete_album',     name='gallery_delete_album'),
    url(r'^delete_picture/(?P<photo_id>\d+)$',    'gallery.views.delete_picture',   name='gallery_delete_picture'),
)
