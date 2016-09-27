# coding=utf-8
from django.contrib import admin
from .models import ContactInfo, Message

admin.site.register((ContactInfo,
                     Message))
