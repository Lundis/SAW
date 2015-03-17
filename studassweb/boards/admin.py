from django.contrib import admin
from .models import Role, BoardType, Board, MemberInBoard, BoardSettings


admin.site.register((Role,
                     BoardType,
                     Board,
                     MemberInBoard,
                     BoardSettings))
