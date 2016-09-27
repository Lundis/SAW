# coding=utf-8
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from base.models import SiteConfiguration, BootswatchTheme, Feedback, CSSOverrideFile, CSSOverrideContent, CSSMap2

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(
    (BootswatchTheme,
     Feedback,
     CSSMap2,
     CSSOverrideContent,
     CSSOverrideFile,
     )
)
