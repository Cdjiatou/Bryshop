from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, password_change, profile_view, register,custom_logout,notifications_view,mark_notification_read
from django.contrib.auth.views import LogoutView



urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', custom_logout, name='logout'),
    

    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    
    # Profil Utilisateur
    path('profile/', profile_view, name='profile'),
    path('profile/password_change/', password_change, name='password_change'), 
    path('profile/update/', views.profile_update, name='profile_update'), 
    path('notifications/', notifications_view, name='notifications_list'), 
    path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
]
