from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from io import BytesIO
from PIL import Image
import os

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
"""Модель для городов"""
class City(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_cities',
        verbose_name="Пользователь",
        blank=True, null=True
    )
    title = models.CharField(
        max_length=255, verbose_name="Название",
    )
    note = models.CharField(
        max_length=255, verbose_name="Комментарий",
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=timezone.now(),
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


"""Модель для разрешения"""
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    codename = models.CharField(max_length=100, unique=True, verbose_name="Кодовое имя")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Разрешение"
        verbose_name_plural = "Разрешения"

"""Модель для группировки разрешений"""
class GroupPermission(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название группы")
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="Права")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Группа разрешения"
        verbose_name_plural = "Группы разрешений"

"""Модель для сотрудников"""
class Employee(models.Model):
    class EmployeePostionChoice(models.TextChoices):
        MANAGER = 'Менеджер', 'Менеджер'
        ADMINISTRATOR = 'Администратор', 'Администратор'
        DIRECTOR = 'Директор', 'Директор'
        CASHIER = 'Кассир', 'Кассир'
        TRAINEE = 'Стажер', 'Стажер'
        COURIER = 'Курьер', 'Курьер'
        SMM = 'Смм', 'Смм'
        OTHER = 'Прочее', 'Прочее'

    city = models.ManyToManyField(
        'City', related_name='city_employees',
        verbose_name="Город"
    )
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        related_name="user_employee",
        verbose_name="Аккаунт пользователя",
        blank=True, null=True, unique=True
    )
    first_name = models.CharField(
        max_length=255, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=100, verbose_name="Номер телефона",
        blank=True, null=True
    )
    selery = models.PositiveBigIntegerField(
        verbose_name='Зарплата', 
        default=0,
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        blank=True, null=True
    )
    address = models.CharField(
        max_length=255, verbose_name="Адрес",
        blank=True, null=True
    )
    date_of_birth = models.DateTimeField(
        verbose_name="Дата рождения",
        blank=True, null=True
    )
    image = models.ImageField(
        upload_to='employee_images/',
        verbose_name="Фотография сотрудника",
        blank=True, null=True
    )
    employee_position = models.CharField(
        max_length=100, verbose_name="Должность", 
        choices=EmployeePostionChoice.choices,
        default=EmployeePostionChoice.OTHER
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True, null=True
    )
    groups = models.ManyToManyField(
        GroupPermission, blank=True, verbose_name="Группа разрещений",
        help_text="Вы можете дать группу разрещений чтобы пользователь имел доступ определенным функциям"
    )
    user_permissions = models.ManyToManyField(
        Permission, blank=True, verbose_name="Права пользователя",
        help_text="Вы можете указать каким разделам будет иметь доступ сотрудник"
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.employee_position}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.format != 'WEBP':
                img = img.convert('RGB')
                webp_io = BytesIO()
                img.save(webp_io, format='WEBP', quality=100)
                webp_name = os.path.splitext(self.image.name)[0] + '.webp'
                self.image.save(webp_name, ContentFile(webp_io.getvalue()), save=False)
                super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем файл изображения перед удалением объекта
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

class PhotosProfile(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='users_employee',
        verbose_name="Пользователь",
        blank=True, null=True
    )
    image = models.ImageField(
        upload_to='user/profie_photos/',
        verbose_name='Фотография',
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

class EmployeeExperience(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='user_experience',
        verbose_name = 'Пользователь',
        blank=True, null=True
    )
    logo = models.ImageField(
        upload_to='user/profile_experience_logo/',
        verbose_name='Логотип компании где работал',
        blank=True, null=True
    )
    position = models.CharField(
        max_length=255,
        verbose_name='Должность компании'
    )
    title = models.CharField(
        max_length = 255,
        verbose_name = 'Название компании'
    )
    year = models.CharField(
        max_length = 255,
        verbose_name = 'Сколько лет проработал'
    )
    location = models.CharField(
        max_length = 255,
        verbose_name = 'Место работы'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'

class EmployeeEducation(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='education',
        verbose_name = 'Пользователь',
        blank=True, null=True
    )
    logo = models.ImageField(
        upload_to='user/education_logo/',
        verbose_name='Лого университета',
        blank=True, null=True
    )
    university = models.CharField(
        max_length = 255,
        verbose_name = 'Название университета'
    )
    year = models.CharField(
        max_length = 255,
        verbose_name = 'Сколько лет обучился'
    )
    location = models.CharField(
        max_length = 255,
        verbose_name = 'Место обучения'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'