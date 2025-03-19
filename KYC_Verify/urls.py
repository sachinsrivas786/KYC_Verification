from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('HR_dashboard/', views.HR_dashboard, name='HR_dashboard'),
    path('get-regions/', views.get_regions, name='get_regions'),
    path('get-units/', views.get_units, name='get_units'), 
    path('get-emp/', views.get_emp, name='get_emp'), 
    path('get_completed_employees/', views.get_completed_employees, name='get_completed_employees'), 
    path("update-is-processed/", views.update_is_processed, name="update-is-processed"),
    path("reports/", views.reports_view, name="reports"),
    path("download-reports/", views.download_reports, name="download_reports"),
]