from django.contrib import admin

from apps.cms.models import Visit

# Register your models here.
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user_agent', 'url_path', 'timestamp')