from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        null=True, blank=True
    )
    def __str__(self):
        return self.username 
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"