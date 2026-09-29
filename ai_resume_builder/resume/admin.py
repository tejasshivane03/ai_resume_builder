"""Admin configuration for resume app."""
from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'updated_at')
    list_filter = ('template', 'created_at')
    search_fields = ('title', 'user__username', 'full_name')
