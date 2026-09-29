"""Models for ATS (Applicant Tracking System) module."""
import json
from django.db import models
from django.contrib.auth.models import User


class ATSResult(models.Model):
    """Stores ATS score analysis for a user's resume against a job description."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ats_results')
    resume_title = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    score = models.IntegerField(default=0)

    # JSON stored fields
    matched_keywords = models.TextField(default='[]')
    missing_keywords = models.TextField(default='[]')
    suggestions = models.TextField(default='[]')
    section_scores = models.TextField(default='{}')

    resume_text = models.TextField(blank=True)
    job_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - ATS {self.score}% ({self.job_title or 'Analysis'})"

    def get_matched_keywords(self):
        try:
            return json.loads(self.matched_keywords)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_missing_keywords(self):
        try:
            return json.loads(self.missing_keywords)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_suggestions(self):
        try:
            return json.loads(self.suggestions)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_section_scores(self):
        try:
            return json.loads(self.section_scores)
        except (json.JSONDecodeError, TypeError):
            return {}
