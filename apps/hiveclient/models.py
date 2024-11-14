from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
        help_text="+996"
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        null=True, blank=True,
        help_text="Адрес пользователя"
    )


    def __str__(self):
        return self.username 
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"