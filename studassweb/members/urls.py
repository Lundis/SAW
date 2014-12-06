from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',
        'members.views.view_members',
        name='members_home'),

    url(r'^apply_membership$',
        'members.views.apply_membership',
        name='members_apply_membership'),
    url(r'^confirm_membership/(?P<member_id>\d+)$',
        'members.views.confirm_membership',
        name='members_confirm_membership'),
    url(r'^deny_membership/(?P<member_id>\d+)$',
        'members.views.deny_membership',
        name='members_deny_membership'),

    url(r'^add_paymentpurpose$',
        'members.views.add_paymentpurpose',
        name='members_add_paymentpurpose'),
    url(r'^edit_paymentpurpose/(?P<paymentpurpose_id>\d+)$',
        'members.views.edit_paymentpurpose',
        name='members_edit_paymentpurpose'),
    url(r'^delete_paymentpurpose/(?P<paymentpurpose_id>\d+)$',
        'members.views.delete_paymentpurpose',
        name='members_delete_paymentpurpose'),
)