"""Admin registration for ATS app."""
from django.contrib import admin
from .models import ATSResult

@admin.register(ATSResult)
class ATSResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'resume_title', 'job_title', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'resume_title', 'job_title']
