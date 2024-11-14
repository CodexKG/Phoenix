from django.db import models

from apps.hiveclient.models import User

# Create your models here.
class Visit(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP-адрес")
    user_agent = models.TextField(verbose_name="User-Agent")
    url_path = models.CharField(max_length=255, verbose_name="URL страницы")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время посещения")

    def __str__(self):
        return f"{self.ip_address} - {self.url_path} - {self.timestamp}"

    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"
        ordering = ['-timestamp']

class Partners(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="user_partners",
        verbose_name="Пользователь"
    )
    title = models.CharField(
        max_length=255, verbose_name="Название",
        blank=True, null=True
    )
    logo = models.ImageField(
        upload_to="partners_images/", 
        verbose_name="Логотип"
    )
    partners_url = models.URLField(
        verbose_name="Ссылка",
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.logo} {self.created}"
    
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
    
class Service(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="user_services",
        verbose_name="Пользователь"
    )
    title = models.CharField(
        max_length=255, verbose_name="Название"
    )
    image = models.ImageField(
        upload_to='services_imeges/',
        verbose_name="Изображение"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class FAQ(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="user_faq",
        verbose_name="Пользователь"
    )
    question = models.CharField(
        max_length=255, verbose_name="Вопрос"
    )
    answer = models.CharField(
        max_length=255, verbose_name="Ответ"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.question}"
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"