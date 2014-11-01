from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'login.views.login_view', name='login'),
    url(r'^logout/', 'login.views.logout_view'),
)