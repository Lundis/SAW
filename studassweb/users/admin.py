from django.contrib import admin
from .models import SAWPermission, UserExtension, KerberosLink, KerberosServer

admin.site.register((SAWPermission, UserExtension, KerberosServer, KerberosLink))
