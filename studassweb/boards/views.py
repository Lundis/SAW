from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseNotAllowed
from django.core.exceptions import SuspiciousOperation
from .models import Board, Role, MemberInBoard, BoardType
from users.decorators import has_permission
from .register import CAN_VIEW_BOARDS, CAN_EDIT_BOARDS
from .forms import RoleForm, BoardTypeForm, BoardForm, BoardMemberForm
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


@has_permission(CAN_VIEW_BOARDS)
def boards_main(request):
    boards = Board.objects.filter().order_by('-year')
    return render(request, 'boards/view_main.html', {'boards': boards, },)


@has_permission(CAN_VIEW_BOARDS)
def view_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        logger.warning('Could not find role with id %s', role_id)
        return HttpResponseNotFound('No role with that id found')

    boardmembers = MemberInBoard.objects.filter(role=role_id)

    return render(request, 'boards/view_role.html',
                  {'role': role,
                   'boardmembers': boardmembers, })


@has_permission(CAN_EDIT_BOARDS)
def add_edit_role(request, role_id=None):
    if role_id is not None:
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            logger.warning('User %s tried to edit nonexistant role id %s', request.user, role_id)
            return HttpResponseNotFound('No such role!')
    else:
        role = None

    form = RoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("boards_view_role", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_role.html', context)


@has_permission(CAN_EDIT_BOARDS)
def delete_role(request, role_id):
    if request.method != 'POST':
        logger.warning('Attempted to access delete_role via other method than POST')
        return HttpResponseNotAllowed(['POST'])
    try:
        role = Role.objects.get(id=role_id)
        name = str(role)
        role.delete()
        messages.success(request, "Role "+name+" was sucessfully deleted!")
        return HttpResponseRedirect(reverse("boards_main"))
    except Role.DoesNotExist:
        raise SuspiciousOperation('User %s tried to delete nonexistant role with id %s' % (request.user,
                                                                                           role_id))
    except models.ProtectedError:
        raise SuspiciousOperation('User %s tried to delete not deletable role with id %s' % (request.user,
                                                                                             role_id))


@has_permission(CAN_VIEW_BOARDS)
def view_board(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        logger.warning('Could not find board with id %s', board_id)
        return HttpResponseNotFound('No board with that id found')

    boardmembers = MemberInBoard.objects.filter(board=board_id)

    return render(request, 'boards/view_board.html', {
        'board': board, 'boardmembers': boardmembers, },)


@has_permission(CAN_EDIT_BOARDS)
def add_edit_board(request, board_id=None):
    if board_id is not None:
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise SuspiciousOperation('User %s tried to edit non-existing board with id %s' % (request.user,
                                                                                               board_id))
    else:
        board = None

    form = BoardForm(request.POST or None, request.FILES, instance=board)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("boards_view_board", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_board.html', context)


@has_permission(CAN_EDIT_BOARDS)
def delete_board(request, board_id):
    if request.method != 'POST':
        logger.warning('Attempted to access delete_board via other method than POST')
        return HttpResponseNotAllowed(['POST', ])

    try:
        board = Board.objects.get(id=board_id)
        name = str(board)
        board.delete()
        messages.success(request, "Board "+name+" was sucessfully deleted!")
        return HttpResponseRedirect(reverse("boards_main"))
    except Board.DoesNotExist:
        raise SuspiciousOperation('User %s tried to delete nonexistant board with id %s' % (request.user,
                                                                                            board_id))
    except models.ProtectedError:
        raise SuspiciousOperation('User %s tried to delete not deletable board with id %s' % (request.user,
                                                                                              board_id))


@has_permission(CAN_VIEW_BOARDS)
def view_boardtype(request, boardtype_id):
    try:
        boardtype = BoardType.objects.get(id=boardtype_id)
    except BoardType.DoesNotExist:
        return HttpResponseNotFound('No board type with id %s found' % boardtype_id)

    boards = Board.objects.filter(boardtype=boardtype_id)

    return render(request, 'boards/view_boardtype.html', {
        'boardtype': boardtype, 'boards': boards, },)


@has_permission(CAN_EDIT_BOARDS)
def add_edit_boardtype(request, boardtype_id=None):
    if boardtype_id is not None:
        try:
            boardtype = BoardType.objects.get(id=boardtype_id)
        except BoardType.DoesNotExist:
            raise SuspiciousOperation('User %s tried to edit non-existing board type with id %s' % (request.user,
                                                                                                    boardtype_id))
    else:
        boardtype = None

    form = BoardTypeForm(request.POST or None, instance=boardtype)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("boards_view_boardtype", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_boardtype.html', context)


@has_permission(CAN_EDIT_BOARDS)
def delete_boardtype(request, boardtype_id):
    if request.method != 'POST':
        logger.warning('Attempted to access delete_boardtype via other method than POST')
        return HttpResponseNotAllowed(['POST', ])
    try:
        boardtype = BoardType.objects.get(id=boardtype_id)
        name = str(boardtype)
        boardtype.delete()
        messages.success(request, "Boardtype "+name+" was sucessfully deleted!")
        return HttpResponseRedirect(reverse("boards_main"))
    except BoardType.DoesNotExist:
        raise SuspiciousOperation('User %s tried to delete nonexistant board type with id %s' % (request.user,
                                                                                                 boardtype_id))
    except models.ProtectedError:
        raise SuspiciousOperation('User %s tried to delete not deletable board type with id %s' % (request.user,
                                                                                                   boardtype_id))


@has_permission(CAN_VIEW_BOARDS)
def view_boardmember(request, boardmember_id):
    try:
        boardmember = MemberInBoard.objects.get(id=boardmember_id)
    except MemberInBoard.DoesNotExist:
        return HttpResponseNotFound('No board member with id %s found' % boardmember_id)

    boards = []
    all_boardmembers = MemberInBoard.objects.filter(member=boardmember.member)
    for bm in all_boardmembers:
        boards.append({'role': bm.role, 'board': bm.board})

    return render(request, 'boards/view_boardmember.html', {
        'boardmember': boardmember, 'boards': boards},)


@has_permission(CAN_EDIT_BOARDS)
def add_edit_boardmember(request, boardmember_id=None):
    if boardmember_id is not None:
        try:
            boardmember = MemberInBoard.objects.get(id=boardmember_id)
        except MemberInBoard.DoesNotExist:
            raise SuspiciousOperation('User %s tried to edit nonexistant board member with id %s' % (request.user,
                                                                                                     boardmember_id))
    else:
        boardmember = None

    form = BoardMemberForm(request.POST or None, request.FILES, instance=boardmember)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("boards_view_boardmember", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_boardmember.html', context)


@has_permission(CAN_EDIT_BOARDS)
def delete_boardmember(request, boardmember_id):
    if request.method != 'POST':
        logger.warning('Attempted to access delete_boardmember via other method than POST')
        return HttpResponseNotAllowed(['POST', ])
    try:
        boardmember = MemberInBoard.objects.get(id=boardmember_id)
        name = str(boardmember)
        boardmember.delete()
        messages.success(request, "Board member "+name+" was sucessfully deleted!")
        return HttpResponseRedirect(reverse("boards_main"))
    except MemberInBoard.DoesNotExist:
        raise SuspiciousOperation('User %s tried to delete nonexistant board member id %s' % (request.user,
                                                                                              boardmember_id))
