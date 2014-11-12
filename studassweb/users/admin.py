from django.contrib import admin
from .models import SAWPermission, UserExtension, LdapLink

admin.site.register(SAWPermission)
admin.site.register(UserExtension)
admin.site.register(LdapLink)
