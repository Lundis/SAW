from django.contrib import admin
from solo.admin import SingletonModelAdmin
from base.models import SiteConfiguration, BootswatchTheme

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(BootswatchTheme)