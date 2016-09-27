# coding=utf-8
from django.conf.urls import url

from . import views
from . import ajax

from django.contrib.auth import views as authviews

urlpatterns = [
    url(r'^login', views.login_view, name='users_login'),
    url(r'^logout$', views.logout_view, name='users_logout'),
    url(r'^register$', views.register, name='users_register'),
    url(r'^register_thanks$', views.register_thanks, name='users_register_thanks'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_]{3,30})$', views.view_profile, name='users_view_profile'),
    url(r'^verify_email/(?P<code>[a-z0-9]{32})', views.verify_email, name='users_verify_email'),

    url(r'^password_reset/$',
        authviews.password_reset,
        {'post_reset_redirect': '/users/password_reset_done/',  # Note we cannot use reverse, url not defined yet
         'template_name': 'users/password_reset/form.html',
         'email_template_name': 'users/password_reset/email.html'},
        name='users_password_reset'),
    url(r'^password_reset_done/$',
        authviews.password_reset_done,
        {'template_name': 'users/password_reset/done.html'},
        name='users_password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        authviews.password_reset_confirm,
        {'post_reset_redirect': '/users/password_reset_complete/',
         'template_name': 'users/password_reset/confirm.html'},
        name='users_password_reset_confirm'),
    url(r'^password_reset_complete/$',
        authviews.password_reset_complete,
        {'template_name': 'users/password_reset/complete.html'},
        name='users_password_reset_complete'),


    url(r'ajax/set_default_group/(?P<username>[a-zA-Z0-9_]{3,30})/(?P<group_name>[a-zA-Z0-9_ ]{3,30})$',
        ajax.set_default_group,
        name='users_ajax_set_default_group'),
]
