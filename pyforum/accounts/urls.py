from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import EmailValidationOnForgotPassword


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
        name="password_reset",
    ),
    path("password/reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/reset/complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
]
