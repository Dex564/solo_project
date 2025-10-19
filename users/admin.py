from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUser(UserAdmin): # UserAdmin - стандартный класс админки для пользователей, мы его кастомизируем
    
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff') # Поля, которые отображаются в списке пользователей
    
    list_filter = ('is_staff', 'is_superuser', 'is_active') # Поля, по которым можно фильтровать
    
    search_fields = ('email', 'first_name', 'last_name') # Поля, по которым можно искать



    # Группировка полей при редактировании пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    # Поля при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    ordering = ('email',)
