from django.contrib import admin
from .models import Member, PaymentPurpose, Payment, CustomEntry, CustomField

admin.site.register(Member)
admin.site.register(PaymentPurpose)
admin.site.register(Payment)
admin.site.register(CustomEntry)
admin.site.register(CustomField)