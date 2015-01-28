from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',                                      'polls.views.home',                 name='polls_home'),
    url(r'^poll/(?P<poll_id>\d+)$',                 'polls.views.view_poll',            name='polls_view_poll'),
    url(r'^add_poll/$',                             'polls.views.add_poll',             name='polls_add_poll'),
    url(r'^remove_poll/(?P<poll_id>\d+)$',          'polls.views.delete_poll',          name='polls_delete_poll'),
    url(r'^edit_poll/(?P<poll_id>\d+)$',            'polls.views.edit_poll',            name='polls_edit_poll'),

    url(r'^choice/(?P<choice_id>\d+)$',             'polls.views.set_user_choice',      name='polls_set_user_choice'),


)
