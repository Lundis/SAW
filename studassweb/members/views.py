from django.shortcuts import render
from django.http import HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from users.decorators import has_permission
from users.models import UserExtension
from .models import Member, PaymentPurpose, CustomField, CustomEntry
from .forms import MemberApplicationForm, PaymentPurposeForm, MemberEditForm
from .register import CAN_VIEW, CAN_EDIT
from base.forms import ConfirmationForm


@has_permission(CAN_VIEW)
def view_members(request):
    rows = []
    extra_columns = CustomField.objects.all()
    for member in Member.objects.all():
        row = [member, []]
        for column in extra_columns:
            value = CustomEntry.objects.get_or_create(field=column, member=member)
            row[1].append(('col-%s' % column.id, value))
        rows.append(row)
    context = {'members_data': rows,
               'extra_columns': extra_columns}
    return render(request, 'members/member_table.html', context)


@has_permission(CAN_EDIT)
def edit_member(request, member_id=None):
    if member_id is not None:
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return HttpResponseBadRequest("Member does not exist")
    else:
        member = None
    form = MemberEditForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("members_home"))
    else:
        context = {'member': member,
                   'form': form}
        return render(request, 'members/edit_member.html', context)


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
    member.deny()
    return HttpResponseRedirect(reverse("members_home"))


@login_required()
def apply_membership(request):
    user_ext = UserExtension.objects.get(user=request.user)
    member = Member.objects.get(user_ext=user_ext)

    if member.confirmed:
        return HttpResponseBadRequest(_("You are already a confirmed member!"))
    elif member.applying:
        return HttpResponseBadRequest(_("You have already applied for membership. " +
                                        "Give the board some time to confirm it or contact them!"))
    else:
        if not user_ext.email_verified:
            return HttpResponseBadRequest(_("You need to verify your email before applying for membership"))
        if not member.can_apply_for_membership:
            return HttpResponseBadRequest(_("You have been banned from applying for membership"))
        context = {}
        form = MemberApplicationForm(request.POST or None, instance=member)
        if form.is_valid():
            form.save()
            member.applying = True
            member.save()
        else:
            context['form'] = form
        return render(request, 'members/member_application.html', context)


@has_permission(CAN_EDIT)
def add_paymentpurpose(request):
    if request.method == 'POST':
        form = PaymentPurposeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/members')  # TODO user probably wants feedback

    form = PaymentPurposeForm()
    context = {'form': form}
    return render(request, 'members/add_paymentpurpose.html', context)


@has_permission(CAN_EDIT)
def edit_paymentpurpose(request, paymentpurpose_id):
    try:
        paymentpurpose = PaymentPurpose.objects.get(id=paymentpurpose_id)
    except PaymentPurpose.DoesNotExist:
        raise Http404

    form = PaymentPurposeForm(instance=paymentpurpose)

    if request.method == 'POST':
        form = PaymentPurposeForm(request.POST, instance=paymentpurpose)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/members')  # TODO user probably wants feedback

    context = {'form': form}
    return render(request, 'members/edit_paymentpurpose.html', context)


@has_permission(CAN_EDIT)
def delete_paymentpurpose(request, paymentpurpose_id):
    try:
        paymentpurpose = PaymentPurpose.objects.get(id=paymentpurpose_id)
    except PaymentPurpose.DoesNotExist:
        raise Http404

    form = ConfirmationForm(request.POST or None)
    if form.is_valid():
        paymentpurpose.delete()
        return HttpResponseRedirect('/members')  # TODO user probably wants feedback
    
    context = {'form': form}
    return render(request, 'members/delete_paymentpurpose.html', context)