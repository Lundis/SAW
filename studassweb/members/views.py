from django.shortcuts import render
from django.http import HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from users.decorators import has_permission
from users.models import UserExtension
from .models import Member, PaymentPurpose, CustomField, CustomEntry, Payment
from .forms import MemberApplicationForm, PaymentPurposeForm, MemberEditForm, CustomFieldForm, PaymentForm
from .register import CAN_VIEW, CAN_EDIT
from base.views import delete_confirmation_view


@has_permission(CAN_VIEW)
def view_members(request):
    rows = []
    extra_columns = CustomField.objects.all()
    payment_purposes = PaymentPurpose.objects.all()
    for member in Member.objects.all():
        row = [member, [], []]
        for field in extra_columns:
            entry, created = CustomEntry.objects.get_or_create(field=field, member=member)
            row[1].append(('col-custom-%s' % field.id, entry))
        for purpose in payment_purposes:
            try:
                payment = Payment.get_latest(purpose=purpose, member=member)
            except Payment.DoesNotExist:
                payment = None
            row[2].append(('col-payment-%s' % purpose.id, payment))
        rows.append(row)
    context = {'members_data': rows,
               'extra_columns': extra_columns,
               'payment_purposes': payment_purposes}
    return render(request, 'members/member_table.html', context)


# =================== Members add/edit/delete ===================

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
def delete_member(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404("Member with id %s not found", member_id)

    return delete_confirmation_view(request,
                                    form_url=reverse("members_delete_member", kwargs={'member_id': member_id}),
                                    redirect_url=reverse("members_home"),
                                    item=member,
                                    template="members/delete_member.html")


# =================== Membership ===================

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


# =================== Custom Fields add/edit/delete ===================

@has_permission(CAN_EDIT)
def edit_custom_field(request, field_id=None):
    if field_id is not None:
        try:
            field = CustomField.objects.get(id=field_id)
        except CustomField.DoesNotExist:
            raise Http404("")
    else:
        field = None

    form = CustomFieldForm(request.POST or None, field)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("members_home"))
    context = {'form': form,
               'field': field}
    return render(request, "members/edit_custom_field.html", context)


@has_permission(CAN_EDIT)
def delete_custom_field(request, field_id):
    try:
        field = PaymentPurpose.objects.get(id=field_id)
    except PaymentPurpose.DoesNotExist:
        raise Http404("Field %s not found" % field_id)

    return delete_confirmation_view(request,
                                    form_url=reverse("members_delete_field"),
                                    item=field,
                                    redirect_url=reverse("members_home"))


# =================== Payment Purpose add/edit/delete ===================

@has_permission(CAN_EDIT)
def add_paymentpurpose(request):
    form = PaymentPurposeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("members_home"))  # TODO user probably wants feedback

    form = PaymentPurposeForm()
    context = {'form': form}
    return render(request, 'members/add_paymentpurpose.html', context)


@has_permission(CAN_EDIT)
def edit_paymentpurpose(request, paymentpurpose_id):
    try:
        paymentpurpose = PaymentPurpose.objects.get(id=paymentpurpose_id)
    except PaymentPurpose.DoesNotExist:
        raise Http404

    form = PaymentPurposeForm(request.POST or None, instance=paymentpurpose)
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

    return delete_confirmation_view(request,
                                    form_url=reverse("members_delete_paymentpurpose"),
                                    item=paymentpurpose,
                                    # TODO: redirect to a page that lists all payment purposes?
                                    redirect_url=reverse("members_home"),
                                    template='members/delete_paymentpurpose.html')


# =================== Payment view/add/delete ===================

@has_permission(CAN_EDIT)
def list_payments(request, member_id):
    """
    Lists all payments for a user
    :param request:
    :param member_id:
    :return:
    """
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404("Member with id %s does not exist" % member_id)
    purposes_payments = ()
    for purpose in PaymentPurpose.objects.all():
        payments = Payment.objects.filter(member=member, purpose=purpose)
        if payments.exists():
            purposes_payments += (purpose, payments),
    context = {'purposes_payments': purposes_payments,
               'member': member}
    return render(request, 'members/payments_list.html', context)


@has_permission(CAN_EDIT)
def add_payment(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404("Member with id %s does not exist" % member_id)
    form = PaymentForm(request.POST or None, user=request.user, member=member)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("members_home"))

    context = {'form': form,
               'member': member}
    return render(request, 'members/payment_add.html', context)


@has_permission(CAN_EDIT)
def delete_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        raise Http404("Payment with id %s does not exist" % payment_id)

    return delete_confirmation_view(request,
                                    form_url=reverse("members_delete_payment"),
                                    item=payment,
                                    redirect_url=reverse("members_list_payments", kwargs={"member_id": payment.member_id}))