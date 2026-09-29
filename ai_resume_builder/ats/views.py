"""Views for ATS checker app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ATSResult
from resume.models import Resume
from resume.services.ats_checker import analyze_ats
from resume.services.resume_parser import extract_text_from_file


@login_required
def ats_checker(request):
    """Render ATS checker form and process resume vs job description comparison."""
    if request.method == 'POST':
        resume_text = ""
        resume_title = "Uploaded Resume"
        job_title = request.POST.get('job_title', '').strip() or "Target Role"
        job_description = request.POST.get('job_description', '').strip()

        # Option A: Selected existing resume
        resume_id = request.POST.get('resume_id')
        if resume_id:
            try:
                selected_resume = Resume.objects.get(pk=resume_id, user=request.user)
                resume_text = selected_resume.get_all_text()
                resume_title = selected_resume.title
            except Resume.DoesNotExist:
                pass

        # Option B: Uploaded file
        if not resume_text and 'resume_file' in request.FILES:
            uploaded_file = request.FILES['resume_file']
            resume_text = extract_text_from_file(uploaded_file)
            resume_title = uploaded_file.name

        # Option C: Pasted raw text
        if not resume_text:
            resume_text = request.POST.get('resume_text', '').strip()

        if not resume_text:
            messages.error(request, "Please select an existing resume, upload a file, or paste your resume text.")
            return redirect('ats_checker')

        if not job_description:
            messages.error(request, "Please provide a job description to compare against.")
            return redirect('ats_checker')

        # Perform ATS analysis
        analysis = analyze_ats(resume_text, job_description)

        # Save result
        ats_result = ATSResult.objects.create(
            user=request.user,
            resume_title=resume_title,
            job_title=job_title,
            score=analysis['score'],
            matched_keywords=str(analysis['matched_keywords']).replace("'", '"'),
            missing_keywords=str(analysis['missing_keywords']).replace("'", '"'),
            suggestions=str(analysis['suggestions']).replace("'", '"'),
            section_scores=str(analysis['section_scores']).replace("'", '"'),
            resume_text=resume_text[:2000],
            job_description=job_description[:2000]
        )

        return redirect('ats_result_detail', pk=ats_result.pk)

    user_resumes = Resume.objects.filter(user=request.user)
    return render(request, 'ats/checker.html', {'resumes': user_resumes})


@login_required
def ats_result_detail(request, pk):
    """View details of an ATS result."""
    result = get_object_or_404(ATSResult, pk=pk, user=request.user)
    context = {
        'result': result,
        'matched': result.get_matched_keywords(),
        'missing': result.get_missing_keywords(),
        'suggestions': result.get_suggestions(),
        'section_scores': result.get_section_scores(),
    }
    return render(request, 'ats/result.html', context)


@login_required
def ats_history(request):
    """View user's ATS check history."""
    results = ATSResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ats/history.html', {'results': results})
