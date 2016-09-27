# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.view_members,
        name='members_home'),
    # =========== Member operations ===========
    url(r'^edit_member/(?P<member_id>\d+)$',
        views.edit_member,
        name='members_edit_member'),
    url(r'^add_member$',
        views.edit_member,
        name='members_add_member'),
    url(r'^delete_member/(?P<member_id>\d+)$',
        views.delete_member,
        name='members_delete_member'),
    # =========== Membership operations ===========
    url(r'^apply_membership$',
        views.apply_membership,
        name='members_apply_membership'),
    url(r'^confirm_membership/(?P<member_id>\d+)$',
        views.confirm_membership,
        name='members_confirm_membership'),
    url(r'^deny_membership/(?P<member_id>\d+)$',
        views.deny_membership,
        name='members_deny_membership'),
    # =========== Custom columns/fields ===========
    url(r'^new_column',
        views.edit_custom_field,
        name='members_create_custom_field'),
    url(r'^edit_column/(?P<field_id>\d+)$',
        views.edit_custom_field,
        name='members_edit_custom_field'),
    url(r'^delete_column/(?P<field_id>\d+)$',
        views.delete_custom_field,
        name='members_delete_custom_field'),
    # =========== Payment purposes ===========
    url(r'^add_paymentpurpose$',
        views.add_paymentpurpose,
        name='members_add_paymentpurpose'),
    url(r'^edit_paymentpurpose/(?P<paymentpurpose_id>\d+)$',
        views.edit_paymentpurpose,
        name='members_edit_paymentpurpose'),
    url(r'^delete_paymentpurpose/(?P<paymentpurpose_id>\d+)$',
        views.delete_paymentpurpose,
        name='members_delete_paymentpurpose'),
    # =========== Payments ===========
    url(r'^view_payments/(?P<member_id>\d+)$',
        views.list_payments,
        name='members_view_payments'),
    url(r'^add_payment/(?P<member_id>\d+)$',
        views.add_payment,
        name='members_add_payment'),
    url(r'^delete_payment/(?P<payment_id>\d+)$',
        views.delete_payment,
        name='members_delete_payment'),
]
