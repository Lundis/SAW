# coding=utf-8
from django import forms
from .models import *


class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ('name',)


class BoardTypeForm(forms.ModelForm):

    class Meta:
        model = BoardType
        fields = ('name',)


class BoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('boardtype', 'year', 'photo')


class BoardMemberForm(forms.ModelForm):

    class Meta:
        model = MemberInBoard
        fields = ('member', 'board', 'role', 'photo')





