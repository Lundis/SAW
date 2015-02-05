from django import forms
from django.utils.translation import ugettext as _
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
        model = BoardMember
        fields = ('member', 'board', 'role', 'photo')





