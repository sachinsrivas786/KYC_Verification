from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('HR_dashboard', views.HR_dashboard, name='HR_dashboard'),
    path('get-regions/', views.get_regions, name='get_regions'),
    path('get-units/', views.get_units, name='get_units'), 
    path('get-emp/', views.get_emp, name='get_emp'), 


]