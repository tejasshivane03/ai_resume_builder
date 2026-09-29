"""Forms for the resume builder."""
from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    """Form for creating / editing a resume's personal info section."""
    class Meta:
        model = Resume
        fields = [
            'title', 'template', 'full_name', 'email', 'phone',
            'location', 'linkedin', 'website', 'summary',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Resume title'}),
            'template': forms.Select(attrs={'class': 'form-input'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City, Country'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'LinkedIn URL'}),
            'website': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Website URL'}),
            'summary': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 4,
                'placeholder': 'Write a short professional summary…',
            }),
        }
