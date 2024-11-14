from django.db import models
from PIL import Image
import os

from apps.hiveclient.models import User
from apps.erp.models import Employee

# Create your models here.
"""Kanban модели"""
class Board(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Название"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )
    owner = models.ForeignKey(
        User, related_name='boards', 
        on_delete=models.CASCADE, verbose_name="Владелец"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

class List(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_lists',
        verbose_name="Пользователь",
        blank=True, null=True
    )
    title = models.CharField(
        max_length=100, verbose_name="Название"
    )
    board = models.ForeignKey(
        Board, related_name='lists', 
        on_delete=models.CASCADE, verbose_name="Доска"
    )
    position = models.IntegerField(
        verbose_name="Позиция",
        blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Список"
        verbose_name_plural = "Списки"

class Card(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="user_cards",
        verbose_name="Пользователь",
        blank=True, null=True
    )
    title = models.CharField(
        max_length=100, verbose_name="Название"
    )
    description = models.TextField(
        blank=True, verbose_name="Описание"
    )
    list = models.ForeignKey(
        List, related_name='card_lists', 
        on_delete=models.CASCADE, 
        verbose_name="Список"
    )
    position = models.IntegerField(
        verbose_name="Позиция",
        blank=True, null=True
    )
    due_date = models.DateTimeField(
        verbose_name="Срок выполнения",
        null=True, blank=True, 
    )
    members = models.ManyToManyField(
        Employee, related_name='employee_cards', 
        blank=True, verbose_name="Участники"
    )
    is_archive = models.BooleanField(
        default=False, verbose_name="Архивация",
        blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )

    def delete(self, *args, **kwargs):
        # Удаляем все вложения, связанные с карточкой
        for attachment in self.card_attachments.all():
            attachment.delete()
        # Теперь удаляем саму карточку
        super(Card, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        ordering = ('position', )  # Карточки будут упорядочены по полю position

class Attachment(models.Model):
    card = models.ForeignKey(
        Card, related_name='card_attachments', 
        on_delete=models.CASCADE,
        verbose_name="Карточка"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    file = models.FileField(
        upload_to='attachments/', verbose_name="Файл"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата загрузки"
    )

    def save(self, *args, **kwargs):
        # Сначала вызываем оригинальный метод save(), чтобы файл был доступен
        super().save(*args, **kwargs)

        # Проверяем, является ли файл изображением
        if self.file and self.file.name.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']:
            # Путь к текущему файлу
            file_path = self.file.path

            # Открываем изображение с помощью Pillow
            image = Image.open(file_path)

            # Создаем имя для нового файла с расширением .webp
            new_file_path = os.path.splitext(file_path)[0] + '.webp'

            # Сохраняем изображение в формате WebP
            image.save(new_file_path, 'webp')

            # Меняем путь к файлу на новый .webp
            self.file.name = os.path.splitext(self.file.name)[0] + '.webp'

            # Удаляем старый файл
            if os.path.exists(file_path):
                os.remove(file_path)

            # Сохраняем снова объект модели с новым файлом
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем файл из файловой системы перед удалением записи из базы данных
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super(Attachment, self).delete(*args, **kwargs)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

class Comment(models.Model):
    card = models.ForeignKey(
        Card, related_name='card_comments', 
        on_delete=models.CASCADE,
        verbose_name="Карточка"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    text = models.TextField(
        verbose_name="Текст"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"Comment by {self.user} on {self.created_at}"
    
    class Meta:
        verbose_name = "Комментарий к карточке"
        verbose_name_plural = "Комментарии к карточкам"