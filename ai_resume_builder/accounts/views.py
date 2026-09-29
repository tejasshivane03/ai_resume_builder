"""Views for authentication and dashboard."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from resume.models import Resume
from ats.models import ATSResult


def logout_view(request):
    """Handle user logout for both GET and POST requests."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')



def accounts_root_view(request):
    """Redirect /accounts or /accounts/ to login or dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """Main dashboard showing user's resumes and ATS results."""
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')[:6]
    ats_results = ATSResult.objects.filter(user=request.user).order_by('-created_at')[:6]
    context = {
        'resumes': resumes,
        'ats_results': ats_results,
        'total_resumes': Resume.objects.filter(user=request.user).count(),
        'total_ats_checks': ATSResult.objects.filter(user=request.user).count(),
    }
    return render(request, 'dashboard/dashboard.html', context)
