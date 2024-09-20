from django.db import models

from apps.hiveclient.models import User

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
    attachments = models.ManyToManyField(
        'Attachment', related_name='cards', 
        blank=True, verbose_name="Вложения"
    )
    members = models.ManyToManyField(
        User, related_name='cards', 
        blank=True, verbose_name="Участники"
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
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

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