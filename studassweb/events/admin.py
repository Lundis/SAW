from django.contrib import admin
from .models import Event, EventItem, EventSignup, ItemInEvent, ItemInSignup


admin.site.register(Event)
admin.site.register(EventItem)
admin.site.register(EventSignup)
admin.site.register(ItemInEvent)
admin.site.register(ItemInSignup)