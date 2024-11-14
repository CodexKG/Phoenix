from django.contrib import admin

from apps.crm.models import Billing

# Register your models here.
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('billing_type', 'phone', 'delivery_price', 'created')