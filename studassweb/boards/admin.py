from django.contrib import admin
from .models import Role, BoardType, Board, BoardMember, BoardSettings


admin.site.register((Role,
                     BoardType,
                     Board,
                     BoardMember,
                     BoardSettings))
