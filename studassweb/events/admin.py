from django.contrib import admin
from .models import Event, EventItem, EventSignup, ItemInEvent, ItemInSignup, EventSettings


admin.site.register((Event,
                     EventItem,
                     EventSignup,
                     ItemInEvent,
                     ItemInSignup,
                     EventSettings))