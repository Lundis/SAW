from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login', 'users.views.login_view', name='users_login'),
    url(r'^logout$', 'users.views.logout_view', name='users_logout'),
    url(r'^register$', 'users.views.register', name='users_register'),
    url(r'^register_thanks$', 'users.views.register_thanks', name='users_register_thanks'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_]{3,30})$', 'users.views.view_profile', name='users_view_profile'),
    url(r'^verify_email/(?P<code>[a-z0-9]{32})', 'users.views.verify_email', name='users_verify_email'),

    url(r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/users/password_reset_done/',  # Note we cannot use reverse, url not defined yet
        'template_name': 'users/password_reset/form.html',
        'email_template_name': 'users/password_reset/email.html'},
        name='users_password_reset'),
    url(r'^password_reset_done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'users/password_reset/done.html'},
        name='users_password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/users/password_reset_complete/',
         'template_name': 'users/password_reset/confirm.html'},
        name='users_password_reset_confirm'),
    url(r'^password_reset_complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'users/password_reset/complete.html'},
        name='users_password_reset_complete'),


    url(r'ajax/set_default_group/(?P<username>[a-zA-Z0-9_]{3,30})/(?P<group_name>[a-zA-Z0-9_ ]{3,30})$',
        'users.ajax.set_default_group',
        name='users_ajax_set_default_group'),
)