from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from .models import Board, Role, MemberInBoard, BoardType
from users import permissions
from .register import CAN_VIEW_BOARDS, CAN_EDIT_BOARDS, CAN_EDIT_ROLES, CAN_EDIT_BOARDTYPES
from .forms import RoleForm, BoardTypeForm, BoardForm, BoardMemberForm
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


def boards_main(request):
    boards = Board.objects.filter().order_by('-year')
    return render(request, 'boards/view_main.html', {'boards': boards, },)


def view_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
        boardmembers = MemberInBoard.objects.filter(role=role_id)

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
    if not permissions.has_user_perm(request.user, CAN_EDIT_ROLES):
            logger.warning('User %s tried to edit role %s', request.user, role_id)
            return HttpResponseForbidden('You don\'t have permission to edit this role!')
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        logger.warning('User %s tried to edit nonexistant role id %s', request.user, role_id)
        return HttpResponseNotFound('No such role!')

    form = RoleForm(instance=role)

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_role", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_role.html', context)


def delete_role(request, role_id):
    if request.method == 'POST':
        try:
            role = Role.objects.get(id=role_id)
            if permissions.has_user_perm(request.user, CAN_EDIT_ROLES):
                name = str(role)
                role.delete()
                messages.success(request, "Role "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("boards_main"))
            else:
                logger.warning('User %s tried to delete role %s', request.user, role)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except Role.DoesNotExist:
            logger.warning('User %s tried to delete nonexistant role id %s', request.user, role_id)
            return HttpResponseNotFound('No such role!')
        except models.ProtectedError:
            logger.warning('User %s tried to delete role %s which is still in use', request.user, role)
            return HttpResponseNotFound('You need to remove all board members with this role first')
    else:
            logger.warning('Attempted to access delete_role via other method than POST')
            return HttpResponseNotAllowed(['POST', ])


def view_board(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
        boardmembers = MemberInBoard.objects.filter(board=board_id)

        return render(request, 'boards/view_board.html', {
            'board': board, 'boardmembers': boardmembers, },)
    except Board.DoesNotExist:
        logger.warning('Could not find board with id %s', board_id)
        return HttpResponseNotFound('No board with that id found')


def add_board(request):
    if not permissions.has_user_perm(request.user, CAN_EDIT_BOARDS):
        logger.warning('User %s tried to add board', request.user)
        return HttpResponseForbidden('You don\'t have permission to add boards!')
    form = BoardForm()

    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_board", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_board.html', context)


def edit_board(request, board_id):
    if not permissions.has_user_perm(request.user, CAN_EDIT_BOARDS):
            logger.warning('User %s tried to edit board id %s', request.user, board_id)
            return HttpResponseForbidden('You don\'t have permission to edit this board!')
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        logger.warning('User %s tried to edit nonexistant board id %s', request.user, board_id)
        return HttpResponseNotFound('No such board!')

    form = BoardForm(instance=board)

    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES, instance=board)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_board", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_board.html', context)


def delete_board(request, board_id):
    if request.method == 'POST':
        try:
            board = Board.objects.get(id=board_id)
            if permissions.has_user_perm(request.user, CAN_EDIT_BOARDS):
                name = str(board)
                board.delete()
                messages.success(request, "Board "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("boards_main"))
            else:
                logger.warning('User %s tried to delete board %s', request.user, board)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except Board.DoesNotExist:
            logger.warning('User %s tried to delete nonexistant board id %s', request.user, board_id)
            return HttpResponseNotFound('No such board!')
        except models.ProtectedError:
            logger.warning('User %s tried to delete board %s which is still in use', request.user, board)
            return HttpResponseNotFound('You need to remove all board members within this board first')
    else:
            logger.warning('Attempted to access delete_board via other method than POST')
            return HttpResponseNotAllowed(['POST', ])


def view_boardtype(request, boardtype_id):
    try:
        boardtype = BoardType.objects.get(id=boardtype_id)
        boards = Board.objects.filter(boardtype=boardtype_id)

        return render(request, 'boards/view_boardtype.html', {
            'boardtype': boardtype, 'boards': boards, },)
    except BoardType.DoesNotExist:
        logger.warning('Could not find board type with id %s', boardtype_id)
        return HttpResponseNotFound('No board type with that id found')


def add_boardtype(request):
    if not permissions.has_user_perm(request.user, CAN_EDIT_BOARDTYPES):
        logger.warning('User %s tried to add boardtype', request.user)
        return HttpResponseForbidden('You don\'t have permission to add board types!')
    form = BoardTypeForm()

    if request.method == 'POST':
        form = BoardTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_boardtype", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_boardtype.html', context)


def edit_boardtype(request, boardtype_id):
    if not permissions.has_user_perm(request.user, CAN_EDIT_BOARDTYPES):
            logger.warning('User %s tried to edit board type %s', request.user, boardtype_id)
            return HttpResponseForbidden('You don\'t have permission to edit this board type!')
    try:
        boardtype = BoardType.objects.get(id=boardtype_id)
    except BoardType.DoesNotExist:
        logger.warning('User %s tried to edit nonexistant bard type id %s', request.user, boardtype_id)
        return HttpResponseNotFound('No such board type!')

    form = BoardTypeForm(instance=boardtype)

    if request.method == 'POST':
        form = BoardTypeForm(request.POST, instance=boardtype)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_boardtype", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_boardtype.html', context)


def delete_boardtype(request, boardtype_id):
    if request.method == 'POST':
        try:
            boardtype = BoardType.objects.get(id=boardtype_id)
            if permissions.has_user_perm(request.user, CAN_EDIT_BOARDTYPES):
                name = str(boardtype)
                boardtype.delete()
                messages.success(request, "Boardtype "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("boards_main"))
            else:
                logger.warning('User %s tried to delete board type %s', request.user, boardtype)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except BoardType.DoesNotExist:
            logger.warning('User %s tried to delete nonexistant board type id %s', request.user, boardtype)
            return HttpResponseNotFound('No such board type!')
        except models.ProtectedError:
            logger.warning('User %s tried to delete board type %s which is still in use', request.user, boardtype)
            return HttpResponseNotFound('You need to remove all boards of this board type first')
    else:
            logger.warning('Attempted to access delete_boardtype via other method than POST')
            return HttpResponseNotAllowed(['POST', ])


def view_boardmember(request, boardmember_id):
    try:
        boardmember = MemberInBoard.objects.get(id=boardmember_id)

        boards = []
        all_boardmembers = MemberInBoard.objects.filter(member=boardmember.member)
        for bm in all_boardmembers:
            boards.append({'role': bm.role, 'board': bm.board})

        return render(request, 'boards/view_boardmember.html', {
            'boardmember': boardmember, 'boards': boards},)
    except MemberInBoard.DoesNotExist:
        logger.warning('Could not find board member with id %s', boardmember_id)
        return HttpResponseNotFound('No board member with that id found')


def add_boardmember(request):
    if not permissions.has_user_perm(request.user, CAN_EDIT_BOARDS):
        logger.warning('User %s tried to add board member', request.user)
        return HttpResponseForbidden('You don\'t have permission to add board members!')
    form = BoardMemberForm()

    if request.method == 'POST':
        form = BoardMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_boardmember", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_boardmember.html', context)


def edit_boardmember(request, boardmember_id):
    if not permissions.has_user_perm(request.user, CAN_EDIT_BOARDS):
            logger.warning('User %s tried to edit board member %s', request.user, boardmember_id)
            return HttpResponseForbidden('You don\'t have permission to edit this board member!')
    try:
        boardmember = MemberInBoard.objects.get(id=boardmember_id)
    except MemberInBoard.DoesNotExist:
        logger.warning('User %s tried to edit nonexistant board member id %s', request.user, boardmember_id)
        return HttpResponseNotFound('No such board member!')

    form = BoardMemberForm(instance=boardmember)

    if request.method == 'POST':
        form = BoardMemberForm(request.POST, request.FILES, instance=boardmember)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("boards_view_boardmember", args=[form.instance.id]))

    context = {'form': form}
    return render(request, 'boards/add_edit_boardmember.html', context)


def delete_boardmember(request, boardmember_id):
    if request.method == 'POST':
        try:
            boardmember = MemberInBoard.objects.get(id=boardmember_id)
            if permissions.has_user_perm(request.user, CAN_EDIT_BOARDS):
                name = str(boardmember)
                boardmember.delete()
                messages.success(request, "Board member "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("boards_main"))
            else:
                logger.warning('User %s tried to delete board member %s', request.user, boardmember)
                return HttpResponseForbidden('You don\'t have permission to remove this!')
        except MemberInBoard.DoesNotExist:
            logger.warning('User %s tried to delete nonexistant board member id %s', request.user, boardmember_id)
            return HttpResponseNotFound('No such board member!')
    else:
            logger.warning('Attempted to access delete_boardmember via other method than POST')
            return HttpResponseNotAllowed(['POST', ])