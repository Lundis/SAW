from django.contrib import admin
from solo.admin import SingletonModelAdmin
from base.models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)