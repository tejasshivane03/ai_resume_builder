"""
Models for the resume builder app.
Stores resume data as structured JSON alongside metadata.
"""
import json
from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    """A single resume created by a user."""

    TEMPLATE_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, default='Untitled Resume')
    template = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default='modern')

    # Personal info
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    summary = models.TextField(blank=True)

    # Structured data stored as JSON
    experience_json = models.TextField(default='[]', help_text='JSON array of work experiences')
    education_json = models.TextField(default='[]', help_text='JSON array of education entries')
    skills_json = models.TextField(default='[]', help_text='JSON array of skills')
    projects_json = models.TextField(default='[]', help_text='JSON array of projects')
    certifications_json = models.TextField(default='[]', help_text='JSON array of certifications')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    # ── Convenience helpers for JSON fields ──────────────────────────
    def get_experience(self):
        try:
            return json.loads(self.experience_json)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_education(self):
        try:
            return json.loads(self.education_json)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_skills(self):
        try:
            return json.loads(self.skills_json)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_projects(self):
        try:
            return json.loads(self.projects_json)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_certifications(self):
        try:
            return json.loads(self.certifications_json)
        except (json.JSONDecodeError, TypeError):
            return []

    def get_all_text(self):
        """Return all resume text concatenated — useful for ATS analysis."""
        parts = [
            self.full_name, self.email, self.phone, self.location,
            self.summary,
        ]
        for exp in self.get_experience():
            parts.extend([
                exp.get('title', ''), exp.get('company', ''),
                exp.get('description', ''),
            ])
        for edu in self.get_education():
            parts.extend([
                edu.get('degree', ''), edu.get('school', ''),
                edu.get('description', ''),
            ])
        parts.extend(self.get_skills())
        for proj in self.get_projects():
            parts.extend([proj.get('name', ''), proj.get('description', '')])
        for cert in self.get_certifications():
            parts.extend([cert.get('name', ''), cert.get('issuer', '')])
        return ' '.join(p for p in parts if p)
