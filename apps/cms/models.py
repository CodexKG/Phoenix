from django.db import models

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