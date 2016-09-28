# coding=utf-8
from django.conf.urls import url

from . import ajax
from . import views

urlpatterns = [
    url('^ajax/give_feedback$',
        ajax.give_feedback,
        name='base_ajax_give_feedback'),

    url('^changelog$',
        views.view_change_log,
        name='base_changelog'),
]
