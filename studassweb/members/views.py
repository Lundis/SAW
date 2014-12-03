from django.shortcuts import render
from django.http import HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from users.decorators import has_permission
from users.models import UserExtension
from .models import Member
from .forms import MemberForm
from .register import CAN_VIEW, CAN_EDIT


@has_permission(CAN_VIEW)
def view_members(request):

    context = {'user_exts': UserExtension.objects.all()}
    return render(request, 'members/member_table.html', context)


@has_permission(CAN_EDIT)
def confirm_membership(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404
    member.confirm()
    return HttpResponseRedirect(reverse("members_home"))


@has_permission(CAN_EDIT)
def deny_membership(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404

    member.delete()
    return HttpResponseRedirect(reverse("members_home"))


@login_required()
def apply_membership(request):
    user = request.user
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        member = None

    if member:
        if member.confirmed:
            return HttpResponseBadRequest(_("You are already a confirmed member!"))
        else:
            return HttpResponseBadRequest(_("You have already applied for membership. " +
                                            "Give the board some time to confirm it or contact them!"))
    user_ext = UserExtension.objects.get(user=user)
    if not user_ext.email_verified:
        return HttpResponseBadRequest(_("You need to verify your email before applying for membership"))
    if not user_ext.can_apply_for_membership:
        return HttpResponseBadRequest(_("You have been banned from applying for membership"))
    context = {}
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save(user)
    else:
        context['form'] = form
    return render(request, 'members/member_application.html', context)