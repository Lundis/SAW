from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login', 'users.views.login_view', name='users_login'),
    url(r'^logout$', 'users.views.logout_view', name='users_logout'),
    url(r'^register$', 'users.views.register', name='users_register'),
    url(r'^view_profile/(?P<username>[a-zA-Z0-9_]{6,30})$', 'users.views.view_profile', name='users_view_profile'),
    url(r'^verify_email', 'users.views.verify_email', name='users_verify_email')
)