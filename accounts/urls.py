from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, register, custom_logout
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    
]
