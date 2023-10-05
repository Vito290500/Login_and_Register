from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import capture_value_view


from . import views


urlpatterns = [
    path("", views.MainPageView.as_view(), name="main-page"),
    path("register/", views.RegisterPageView.as_view(), name="register-page"),
    path("email_verify/", views.EmailValidationView.as_view(), name="email-validation-check"),
    path("success/", views.SuccessView, name="success"),
    path("unsuccess/", views.UnSuccessView, name="unsuccess"),
    path('capture-value/', capture_value_view.as_view(), name='capture_value'),
    path("check_email/", views.CheckEmailView, name="check-email"),
    path("reset_password", views.ResetPasswordView.as_view(), name="reset_password"),
    path("confirm_update_password", views.ConfirmUpdatePass, name="update-confirm-password")
]