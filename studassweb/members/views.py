from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from users.decorators import has_permission
from users.groups import put_user_in_default_group, MEMBER
from .models import Member
from .forms import MemberForm
from .register import CAN_VIEW


@has_permission(CAN_VIEW)
def view_members(request):
    pass


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

    context = {}
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        put_user_in_default_group(user, MEMBER)
    else:
        context['form'] = form
    return render(request, 'members/member_application.html', context)