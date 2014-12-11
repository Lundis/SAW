from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',                                      'polls.views.home',                 name='polls_home'),
    url(r'^poll/(?P<poll_id>\d+)$',                 'polls.views.view_poll',            name='polls_view_poll'),
    url(r'^choice/(?P<choice_id>\d+)$',             'polls.views.set_user_choice',      name='polls_set_user_choice'),


)
