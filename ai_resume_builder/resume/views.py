"""Views for the resume builder."""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Resume
from .forms import ResumeForm
from .services.ai_service import improve_summary, improve_experience, suggest_skills
from .services.pdf_generator import generate_pdf


@login_required
def resume_list(request):
    """Show list of user's resumes."""
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume/templates.html', {'resumes': resumes})


@login_required
def resume_create(request):
    """Create a new blank resume and redirect to builder."""
    resume = Resume.objects.create(
        user=request.user,
        title='Untitled Resume',
        full_name=f"{request.user.first_name} {request.user.last_name}".strip(),
        email=request.user.email,
    )
    return redirect('resume_builder', pk=resume.pk)


@login_required
def resume_builder(request, pk):
    """Main builder page for editing a resume."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume saved successfully!')
            return redirect('resume_builder', pk=pk)
    else:
        form = ResumeForm(instance=resume)

    context = {
        'form': form,
        'resume': resume,
        'experience': resume.get_experience(),
        'education': resume.get_education(),
        'skills': resume.get_skills(),
        'projects': resume.get_projects(),
        'certifications': resume.get_certifications(),
    }
    return render(request, 'resume/builder.html', context)


@login_required
@require_POST
def save_section(request, pk):
    """AJAX endpoint – save a JSON section of the resume."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    section = data.get('section')
    content = data.get('content')

    field_map = {
        'experience': 'experience_json',
        'education': 'education_json',
        'skills': 'skills_json',
        'projects': 'projects_json',
        'certifications': 'certifications_json',
    }

    if section not in field_map:
        return JsonResponse({'error': 'Unknown section'}, status=400)

    setattr(resume, field_map[section], json.dumps(content))
    resume.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def ai_improve(request, pk):
    """AJAX endpoint – improve text with AI."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    action = data.get('action')
    text = data.get('text', '')
    job_title = data.get('job_title', '')

    if action == 'improve_summary':
        result = improve_summary(text, job_title)
    elif action == 'improve_experience':
        result = improve_experience(text, job_title)
    elif action == 'suggest_skills':
        current = data.get('current_skills', [])
        result = suggest_skills(job_title, current)
        return JsonResponse({'skills': result})
    else:
        return JsonResponse({'error': 'Unknown action'}, status=400)

    return JsonResponse({'improved_text': result})


@login_required
def resume_preview(request, pk):
    """Full-page preview of the resume."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    context = {
        'resume': resume,
        'experience': resume.get_experience(),
        'education': resume.get_education(),
        'skills': resume.get_skills(),
        'projects': resume.get_projects(),
        'certifications': resume.get_certifications(),
    }
    return render(request, 'resume/preview.html', context)


@login_required
def resume_download_pdf(request, pk):
    """Download resume as PDF."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    pdf_bytes = generate_pdf(resume)
    if pdf_bytes is None:
        messages.error(request, 'PDF generation failed. Please install WeasyPrint.')
        return redirect('resume_preview', pk=pk)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    filename = f"{resume.title.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def resume_delete(request, pk):
    """Delete a resume."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted.')
        return redirect('resume_list')
    return redirect('resume_list')
