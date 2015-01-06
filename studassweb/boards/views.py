from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from .models import Board, Role, BoardMember, BoardType
from users import permissions
from .register import CAN_VIEW_BOARDS, CAN_EDIT_BOARDS, CAN_EDIT_ROLES, CAN_EDIT_BOARDTYPES
from .forms import RoleForm
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger(__name__)


def boards_main(request):
    boards = Board.objects.filter().order_by('-year')

    show_add_buttons = True
    return render(request, 'boards/view_main.html', {
        'boards': boards, 'show_add_buttons': show_add_buttons},)


def view_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
        boardmembers = BoardMember.objects.filter(role=role_id) #TODO ? .order_by('-year')

        return render(request, 'boards/view_role.html', {
            'role': role, 'boardmembers': boardmembers, },)
    except Role.DoesNotExist:
        logger.warning('Could not find role with id %s', role_id)
        return HttpResponseNotFound('No role with that id found')


def add_role(request):
    if not permissions.has_user_perm(request.user, CAN_EDIT_ROLES):
        logger.warning('User %s tried to add role', request.user)
        return HttpResponseForbidden('You don\'t have permission to add roles!')
    form = RoleForm()

    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_role", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_role.html', context)


def edit_role(request, role_id):
    return HttpResponseNotFound('Not implemented')


def delete_role(request, role_id):
    return HttpResponseNotFound('Not implemented')


def view_board(request, board_id):
    return HttpResponseNotFound('Not implemented')


def add_board(request):
    return HttpResponseNotFound('Not implemented')


def edit_board(request, board_id):
    return HttpResponseNotFound('Not implemented')


def delete_board(request, board_id):
    return HttpResponseNotFound('Not implemented')


def view_boardtype(request, boardtype_id):
    return HttpResponseNotFound('Not implemented')


def add_boardtype(request):
    return HttpResponseNotFound('Not implemented')


def edit_boardtype(request, boardtype_id):
    return HttpResponseNotFound('Not implemented')


def delete_boardtype(request, boardtype_id):
    return HttpResponseNotFound('Not implemented')


def view_boardmember(request, boardmember_id):
    return HttpResponseNotFound('Not implemented')


def add_boardmember(request):
    return HttpResponseNotFound('Not implemented')


def edit_boardmember(request, boardmember_id):
    return HttpResponseNotFound('Not implemented')


def delete_boardmember(request, boardmember_id):
    return HttpResponseNotFound('Not implemented')