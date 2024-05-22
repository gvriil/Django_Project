from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from .views import RegisterView, ProfileView, CustomLoginView, forgot_password, PasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/forgot_password/', PasswordResetView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
