from django.urls import path

from users.apps import UsersConfig
from .views import UserRegisterView

app_name = UsersConfig.name

app_name = 'catalog'

urlpatterns = [
    path('register/', UserRegisterView.as_view, name='register'),
    path('login/', UserLoginView.as_view, name='register'),
    path('register/', UserRegisterView.as_view, name='register'),

]
