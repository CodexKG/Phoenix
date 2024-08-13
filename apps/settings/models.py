from django.db import models

from django_resized.forms import ResizedImageField

# Create your models here.
class Setting(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название сайта"
    )
    description = models.TextField(
        max_length=400,
        verbose_name="Описание",
        blank=True, null=True
    )
    logo = ResizedImageField(
        force_format="WEBP", quality=100, 
        upload_to='uploads/', verbose_name="Фотография", 
        blank=True, null=True
    )
    mobile_logo = ResizedImageField(
        force_format="WEBP", quality=100, 
        upload_to='uploads/', verbose_name="Фотография", 
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Почта",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
        blank=True, null=True
    )
    address = models.CharField(
        max_length=300,
        verbose_name="Адрес",
        blank=True, null=True
    )
    facebook = models.URLField(
        verbose_name="Facebook",
        blank=True, null=True
    )
    instagram = models.URLField(
        verbose_name="Instagram",
        blank=True, null=True
    )
    tiktok = models.URLField(
        verbose_name="TikTok",
        blank=True, null=True
    )
    telegram = models.URLField(
        verbose_name="Telegram",
        blank=True, null=True
    )
    whatsapp = models.URLField(
        verbose_name="WhatsApp",
        blank=True, null=True
    )
    telegram_group_chat_id = models.IntegerField(
        verbose_name="ID чата telegram",
        blank=True, null=True
    )
    menu_telegram_group_chat_id = models.IntegerField(
        verbose_name="ID чата menu telegram",
        blank=True, null=True
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона"
    )
    message = models.CharField(
        max_length=500,
        verbose_name="Сообщение",
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

class PageVisit(models.Model):
    date = models.DateField(
        auto_now_add=True, verbose_name="Дата"
    )
    visits = models.PositiveIntegerField(
        default=0, verbose_name="Количество посещений"
    )

    def __str__(self):
        return f"Посещения за {self.date}: {self.visits}"

    class Meta:
        abstract = True

class MainPageVisit(PageVisit):
    class Meta:
        verbose_name = "Посещение главной страницы"
        verbose_name_plural = "Посещения главной страницы"

class MenuVisit(PageVisit):
    class Meta:
        verbose_name = "Посещение меню"
        verbose_name_plural = "Посещения меню"

class FAQ(models.Model):
    question = models.CharField(
        max_length=255,
        verbose_name="Вопрос"
    )
    answer = models.CharField(
        max_length=255,
        verbose_name="Ответ"
    )

    def __str__(self):
        return f"{self.question} {self.answer}"
    
    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"

class Promotions(models.Model):
    title = models.CharField(
        max_length=55,
        verbose_name="Заголовок"
    )
    sub_title = models.CharField(
        max_length=55,
        verbose_name="Под загаловок",
        blank=True,
        null=True
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Текст промоакции",
        blank=True,
        null=True
    )
    image = ResizedImageField(
        force_format="WEBP", quality=100, 
        upload_to='uploads/', verbose_name="Фотография", 
        blank=True, null=True
    )
    url = models.URLField(
        verbose_name="Ссылка на промоакцию"
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Промоакция"
        verbose_name_plural = "Промоакции"

class PromoCode(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        blank=True, null=True
    )
    code = models.CharField(
        max_length=200,
        verbose_name="Код"
    )
    quantity = models.SmallIntegerField(
        verbose_name="Количество"
    )
    amount = models.IntegerField(
        verbose_name="Сумма промокода"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания промокода"
    )

    def __str__(self):
        return self.code 
    
    class Meta:
        verbose_name = "Промокод (скидка на сайте)"
        verbose_name_plural = "Промокоды (скидки на сайте)"
        
class AboutUs(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок страницы О нас'
    )
    description = models.CharField(
        max_length=855,
        verbose_name='Описание страницы О нас'
    )
    image = ResizedImageField(
        force_format="WEBP", quality=100, 
        upload_to='uploads/', verbose_name="Фотография", 
        blank=True, null=True
    )
    exp = models.CharField(
        max_length=55,
        verbose_name='Опыт работы'
    )
    promo_title = models.CharField(
        max_length=255,
        verbose_name='Заголовок промо'
    )
    promo_desc = models.CharField(
        max_length=255,
        verbose_name='Описание промо'
    )
    promo_video = models.FileField(
        upload_to='about_us/',
        verbose_name='Промо видео'
    )
    promo_image = models.FileField(
        upload_to='about_us/',
        verbose_name='Промо фото '
    )
    
    def __str__(self):
        return f"О нас: {self.id}"
    
    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        
class FactsAboutUs(models.Model):
    number = models.CharField(
        max_length=2,
        verbose_name='Номер факта'
    )
    title = models.CharField(
        max_length=55,
        verbose_name='Факт'
    )
    text = models.CharField(
        max_length=150,
        verbose_name='Текст факта'
    )

class Employees(models.Model):
    name = models.CharField(
        max_length=55,
        verbose_name='ФИО сотрудника'
    )
    job_title = models.CharField(
        max_length=55,
        verbose_name='Должность'
    )
    image = ResizedImageField(
        force_format="WEBP", quality=100, 
        upload_to='uploads/', verbose_name="Фотография", 
        blank=True, null=True
    )
    tweeter = models.URLField(
        'Ссылка на Tweeter',
        blank=True, null=True
    )
    instagram = models.URLField(
        'Ссылка на Instagram',
        blank=True, null=True
    )
    facebook = models.URLField(
        'Ссылка на Facebook',
        blank=True, null=True
    )
    telegram = models.URLField(
        'Ссылка на telegram',
        blank=True, null=True
    )
    
    def __str__(self):
        return f"{self.name} - {self.job_title}"
    
    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        
class Messages(models.Model):
    name = models.CharField(
        max_length=55,
        verbose_name='Имя отправителя'
    )
    email = models.EmailField(
        verbose_name='Имя отправителя'
    )
    message = models.CharField(
        max_length=500,
        verbose_name='Текст отправителя'
    )
    
    def __str__(self):
        return f"{self.name} - {self.message[0:10]}"
    
    class Meta:
        verbose_name = 'Сообщение от пользователя'
        verbose_name_plural = 'Сообщения от пользователей'