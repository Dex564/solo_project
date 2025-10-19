from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    
    # Представление для входа пользователя.
    # Используем встроенное представление LoginView, оно уже знает как обрабатывать логин.
    
    template_name = 'users/login.html'  # Указываем наш шаблон
    redirect_authenticated_user = True  # Если пользователь уже вошёл, перенаправляем его

class SignUpView(CreateView):
    
    # Представление для регистрации нового пользователя.
    # Наследуемся от CreateView - универсального представления для создания объектов.
    
    form_class = CustomUserCreationForm  # Используем нашу кастомную форму
    template_name = 'users/signup.html'  # Шаблон для регистрации
    success_url = '/'  # Куда перенаправлять после успешной регистрации
    
    def form_valid(self, form):
        
        # Вызывается когда форма валидна.
        # Сохраняем пользователя и автоматически входим его в систему.
        
        user = form.save()  # Сохраняем пользователя в базу
        login(self.request, user)  # Автоматически входим пользователя
        return redirect(self.success_url)  # Перенаправляем на главную
