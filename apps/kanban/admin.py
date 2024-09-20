from django.contrib import admin

from apps.kanban import models

# Register your models here.
@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'owner')

@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'position', 'created_at', 'updated_at')

@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'position', 'due_date', 'created_at', 'updated_at')

@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'file', 'created_at')

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'text', 'created_at', 'updated_at')