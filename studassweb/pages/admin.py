from django.contrib import admin
from .models import InfoPage, InfoCategory, InfoPageEdit

admin.site.register(InfoCategory)
admin.site.register(InfoPage)
admin.site.register(InfoPageEdit)
