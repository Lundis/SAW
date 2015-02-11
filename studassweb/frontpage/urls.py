from django.conf.urls import patterns, url

# / is defined in studassweb.urls
# These will be prepended by /frontpage/

urlpatterns = patterns('',
    url(r'^edit$',
        'frontpage.views.frontpage',
        {'edit_mode': True},
        name='frontpage_edit'),

    url(r'^move_item$', 'frontpage.ajax.move_item', name='frontpage_move_item')
)