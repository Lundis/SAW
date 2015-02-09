from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('^ajax/give_feedback$',
        'base.ajax.give_feedback',
        name='base_ajax_give_feedback'),
)