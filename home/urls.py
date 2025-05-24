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
    path('pcos', views.pcos, name='pcos'),
    path('report', views.report, name='report'),
]
