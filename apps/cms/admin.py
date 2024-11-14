from django.contrib import admin

from apps.cms.models import Visit, Partners, Service, FAQ

# Register your models here.
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user_agent', 'url_path', 'timestamp')

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'partners_url', 'created')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')