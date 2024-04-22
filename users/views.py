import random
import string

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm, PasswordResetRequestForm
from users.models import User


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем, вы зарегистрированы!',
            message='Вы успешно зарегистрированы на нашем сайте.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],  # Правильное имя аргумента
            fail_silently=False,  # Добавлено для обработки возможных ошибок отправки
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def forgot_password(request):
    request.user.set_password()
    request.user.save()
    return redirect(reverse('users:login'))


class PasswordResetView(View):
    form_class = PasswordResetRequestForm
    template_name = 'users/password_reset_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                user.set_password(new_password)
                user.save()
                send_mail(
                    'Восстановление пароля',
                    f'Ваш новый пароль: {new_password}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Новый пароль отправлен на ваш email.')
                return redirect('users:login')
            else:
                messages.error(request, 'Пользователь с таким email не найден.')
        return render(request, self.template_name, {'form': form})
