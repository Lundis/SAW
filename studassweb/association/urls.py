from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url("^$", "association.views.main", name="association_main"),
)