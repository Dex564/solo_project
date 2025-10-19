from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    # Форма для регистрации нового пользователя.
    # Наследуемся от UserCreationForm чтобы получить логику проверки паролей.

    class Meta:
        model = CustomUser
        fields = ('email',)  # Только email, пароли уже есть в родительской форме


class CustomUserChangeForm(UserChangeForm):

    # Форма для редактирования существующего пользователя.
    # Используется в админке.

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
