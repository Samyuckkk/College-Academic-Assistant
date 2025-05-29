"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('studentDashboard/', views.studDash, name="studDash"),
    path('professorDasboard/', views.profDash, name="profDash"),
    path('cabinLocation/', views.cabinLoc, name="cabinLoc"),
    path('studentAppointment/', views.studApp, name="studApp"),
    path('professorAppointment/', views.profApp, name="profApp"),
    path('adminPage/', views.adminDash, name="adminDash"),
    path('loginroles/', views.loginRoles, name="loginRoles"),
    path('redirect/', views.role_based_redirect, name='role_redirect'),
    path('create-appointment/', views.create_appointment, name='create_appointment'),

    path('semesters/', views.semesters, name="semesters"),
    path('accept-appointment/', views.accept_appointment, name='accept_appointment'),
    path('acceptedAppointments/', views.accepted_appointments, name='acceptedAppointments'),
    path('Student-Accepted-Appointments', views.stud_accepted, name='stud_accepted'),


    path('semester-subjects/<int:sem_number>/', views.sem_subjects, name='sem_subjects'),
    path('edit-subject/<int:id>/', views.edit_subject, name='edit_subject'),


    path('specializations', views.specializations, name='specializations'),
]

