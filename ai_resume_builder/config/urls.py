"""
Root URL configuration for AI Resume Builder.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from accounts import views as accounts_views


def root_redirect(request):
    """Redirect root path / to dashboard or login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


urlpatterns = [
    path('', root_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', accounts_views.dashboard_view, name='dashboard'),
    path('resume/', include('resume.urls')),
    path('ats/', include('ats.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
