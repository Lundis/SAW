from django.contrib import admin
from .models import ContactInfo, Message

admin.site.register(ContactInfo)
admin.site.register(Message)