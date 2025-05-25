"""
URL configuration for home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
import home
from django.contrib import admin
from django.urls import path
from home import views

# đăng kí các app con trong django
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('profile', views.complete_profile, name='profile'),
    path("dashboard", views.user_dashboard, name="dashboard"),
    path('logout', views.user_logout, name='logout'),
    path("health_prediction", views.health_prediction, name="health_prediction"),
    path('mental_disorder', views.mental_disorder, name="mental_disorder"),
    path('add_reminder/', views.add_reminder, name='add_reminder'),
    path('reminder_history/', views.reminder_history, name='reminder_history'),
    path('reminder/<int:reminder_id>/edit/', views.edit_reminder, name='edit_reminder'),
    path('reminder/<int:reminder_id>/delete/', views.delete_reminder, name='delete_reminder'),
    path('reminder/<int:reminder_id>/done/', views.mark_as_done, name='mark_as_done'),
    path('reminder/<int:reminder_id>/mark_completed/', views.mark_as_completed, name='mark_as_completed'),
    path('appointment_scheduled', views.appointment_scheduled, name='appointment_scheduled'),
    path('appointment_history/', views.appointment_history, name='appointment_history'),
    path("api/available-doctors/", views.get_available_doctors, name="available_doctors"),
    path("report", views.report, name="report"),
    path("test_history", views.test_history, name="test_history"),
]
