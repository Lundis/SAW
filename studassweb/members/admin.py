from django.contrib import admin
from .models import Member, PaymentPurpose, Payment, CustomEntry, CustomField

admin.site.register((Member,
                     PaymentPurpose,
                     Payment,
                     CustomEntry,
                     CustomField))