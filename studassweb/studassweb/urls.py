from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studassweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('frontpage.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^example/', include('example.urls')),
    url(r'^exams/', include('exams.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^links/', include('exams.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^settings/', include('settings.urls')),
)
