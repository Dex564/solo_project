from django.db import models
from django.utils.translation import gettext_lazy as _    # нужно чтобы был перевод на другие языки
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # Убираем обязательность username (он нам не нужен для входа по email), пока не понял зачем надо

    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,  # Разрешаем пустое значение
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )


    def __str__(self):
        return self.email
    




