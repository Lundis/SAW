from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import InstallProgress

admin.site.register(InstallProgress, SingletonModelAdmin)