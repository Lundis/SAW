from django.conf.urls import url
from . import views
from . import ajax
# / is defined in studassweb.urls
# These will be prepended by /frontpage/

urlpatterns = [
    url(r'^edit$',
        views.frontpage,
        {'edit_mode': True},
        name='frontpage_edit'),

    url(r'^move_item$', ajax.move_item, name='frontpage_move_item')
]