from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login', 'users.views.login_view', name='users_login'),
    url(r'^logout$', 'users.views.logout_view', name='users_logout'),
    url(r'^register$', 'users.views.register', name='users_register'),
    url(r'^register_thanks$', 'users.views.register_thanks', name='users_register_thanks'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_]{3,30})$', 'users.views.view_profile', name='users_view_profile'),
    url(r'^verify_email/(?P<code>[a-z0-9]{32})', 'users.views.verify_email', name='users_verify_email'),

    url(r'ajax/set_default_group/(?P<username>[a-zA-Z0-9_]{3,30})/(?P<group_name>[a-zA-Z0-9_ ]{3,30})$',
        'users.ajax.set_default_group',
        name='users_ajax_set_default_group'),
)