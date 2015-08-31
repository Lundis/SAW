from django.contrib import admin
from solo.admin import SingletonModelAdmin
from base.models import SiteConfiguration, BootswatchTheme, Feedback, CSSMap, CSSOverrideFile, CSSOverrideContent

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(
    (BootswatchTheme,
     Feedback,
     CSSMap,
     CSSOverrideContent,
     CSSOverrideFile,
     )
)
