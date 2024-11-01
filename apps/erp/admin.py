from django.contrib import admin

from apps.erp import models

# Register your models here.
class EmployeePhotosTabularInline(admin.TabularInline):
    model = models.PhotosProfile
    extra = 0

class EmployeeExperienceTabularInline(admin.TabularInline):
    model = models.EmployeeExperience
    extra = 0

class EmployeeEducationTabularInline(admin.TabularInline):
    model = models.EmployeeEducation
    extra = 0

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_position', 'created')
    inlines = (EmployeePhotosTabularInline, EmployeeExperienceTabularInline, EmployeeEducationTabularInline)