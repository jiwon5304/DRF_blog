from django.urls import path
from .views import(
    RegisterUserView,
    LoginUserView,
    CurrentUserView
)

urlpatterns = [
    path(r'auth/register', RegisterUserView.as_view()),
    path(r'auth/login', LoginUserView.as_view()),
    path(r'auth/me', CurrentUserView.as_view()),
]