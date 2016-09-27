# coding=utf-8
from django.conf.urls import url

from . import ajax

urlpatterns = [
    url('^ajax/give_feedback$',
        ajax.give_feedback,
        name='base_ajax_give_feedback'),
]
