"""URL patterns for the resume app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('create/', views.resume_create, name='resume_create'),
    path('<int:pk>/build/', views.resume_builder, name='resume_builder'),
    path('<int:pk>/save-section/', views.save_section, name='resume_save_section'),
    path('<int:pk>/ai-improve/', views.ai_improve, name='resume_ai_improve'),
    path('<int:pk>/preview/', views.resume_preview, name='resume_preview'),
    path('<int:pk>/download/', views.resume_download_pdf, name='resume_download_pdf'),
    path('<int:pk>/delete/', views.resume_delete, name='resume_delete'),
]
