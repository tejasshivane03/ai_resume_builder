"""URL configuration for ATS module."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ats_checker, name='ats_checker'),
    path('result/<int:pk>/', views.ats_result_detail, name='ats_result_detail'),
    path('history/', views.ats_history, name='ats_history'),
]
