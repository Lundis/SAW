from django.contrib import admin
from .models import Role, BoardType, Board, BoardMember


admin.site.register(Role)
admin.site.register(BoardType)
admin.site.register(Board)
admin.site.register(BoardMember)
