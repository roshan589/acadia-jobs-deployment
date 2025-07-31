from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("accounts/", include('django.contrib.auth.urls')),
    path("signup/", views.signup, name="signup"),
    path("verify-account/", views.verify_email, name="verify_email"),
    path('change-password/', views.passChangeView, name='password_change'),
    path('forgot-password/', views.password_reset_request, name='password_reset'),
    path('password-reset-done/', views.password_email, name='password_email'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', views.logoutView, name='logout'),
]