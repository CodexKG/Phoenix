from django.db import models
from django.utils.translation import gettext as _
import uuid

from apps.hiveclient.models import User

# Create your models here.
class Billing(models.Model):
    class BillingReceiptTypeChoices(models.TextChoices):
        PICKUP = 'Самовывоз', _('Самовывоз')
        DELIVERY = 'Доставка', _('Доставка')
        UNKNOWN = 'Неизвестно', _('Неизвестно')

    class BillingStatusChoices(models.TextChoices):
        INBACKET = 'В корзине', _('В корзине')
        ISSUED = 'Оформлен', _('Оформлен')
        PAID = 'Оплачен', _('Оплачен')
        DELIVERED = 'Доставлен', _('Доставлен')
        RETURN = 'Возврат', _('Возврат')
        UNKNOWN = 'Неизвестно', _('Неизвестно')

    class BillingPaymentStatusChoices(models.TextChoices):
        PAID = 'Оплачен', _('Оплачен')
        NOTPAID = 'Не оплачен', _('Не оплачен')
        ERROR = 'Ошибка', _('Ошибка')
        PERFORMED = 'В исполнении', _('В исполнении')

    class BillingPaymentChoices(models.TextChoices):
        CASH_IN_STORE = 'Наличными в магазине', _('Наличными в магазине')
        CASH_TO_COURIER = 'Наличными курьеру', _('Наличными курьеру')
        PAYMENT_CARD_TO_COURIER = 'Оплата картой курьеру', _('Оплата картой курьеру')
        PAYMENT_TRANSFER = 'Оплата начислением', _('Оплата начислением')
        PAYMENT_INSTALLMENTS = 'Оплата в рассрочку', _('Оплата в рассрочку')
        PAYMENT_VISA = 'Картой Visa', _('Картой Visa')
        MBANK = 'Мбанк', _('Мбанк')
        OPTIMA24 = 'Optima 24', _('Optima 24')
        ODENGI = 'О! Деньги',_('О! Деньги')
        BAKAI24 = 'Bakai 24',_('Bakai 24')
        ERROR = 'Ошибка', _('Ошибка')
        UNKNOWN = 'Неизвестно', _('Неизвестно')

    class BillingTypeChoices(models.TextChoices):
        LEADGENERATION = 'Лидогенерация', _('Лидогенерация')
        BILLING = 'Биллинг', _('Биллинг')

    billing_type = models.CharField(
        max_length=100, choices=BillingTypeChoices.choices,
        default=BillingTypeChoices.LEADGENERATION,
        verbose_name=_('Тип биллинга')
    )
    billing_receipt_type = models.CharField(
        max_length=100, choices=BillingReceiptTypeChoices.choices,
        default=BillingReceiptTypeChoices.UNKNOWN,
        verbose_name=_('Вид получения товара'),
    )
    billing_status = models.CharField(
        max_length=100, choices=BillingStatusChoices.choices,
        default=BillingStatusChoices.INBACKET,
        verbose_name=_('Статус заказа')
    )
    billing_payment_status = models.CharField(
        max_length=100, choices=BillingPaymentStatusChoices.choices,
        default=BillingPaymentStatusChoices.PERFORMED,
        verbose_name=_('Статус оплаты')
    )
    billing_payment = models.CharField(
        max_length=100, choices=BillingPaymentChoices.choices,
        default=BillingPaymentChoices.UNKNOWN,
        verbose_name=_('Способы оплаты')
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name="billing_user",
        verbose_name="Пользователь",
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Почта",
        blank=True, null=True
    )
    first_name = models.CharField(
        max_length=255, verbose_name="Имя",
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=255, verbose_name="Телефонный номер",
        blank=True, null=True
    )
    payment_code = models.CharField(
        max_length=20,
        verbose_name="Код оплаты",
        blank=True, null=True
    )
    delivery_from = models.CharField(
        max_length=250, verbose_name="Доставка откуда",
        blank=True, null=True
    )
    delivery_to = models.CharField(
        max_length=250, verbose_name="Доставка куда",
        blank=True, null=True
    )
    type_product = models.CharField(
        max_length=500, verbose_name="Вид товара",
        blank=True, null=True
    )
    length_product = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Длина",
        blank=True, null=True
    )
    width_product = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Ширина",
        blank=True, null=True
    )
    height_product = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Высота",
        blank=True, null=True
    )
    weight_product = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Вес товара",
        blank=True, null=True
    )
    volume_product = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Объем куб",
        blank=True, null=True
    )
    country = models.CharField(
        max_length=255, 
        verbose_name="Страна",
        blank=True, null=True,
        default="Кыргызстан"
    )
    region = models.CharField(
        max_length=255,
        verbose_name="Регион",
        blank=True, null=True
    )
    street = models.CharField(
        max_length=255, 
        verbose_name="Улица",
        blank=True, null=True
    )
    apartment = models.CharField(
        max_length=255,
        verbose_name="Квартира",
        blank=True, null=True
    )
    zip_code = models.CharField(
        max_length=20,
        verbose_name="Индекс",
        blank=True, null=True
    )
    note = models.TextField(
        verbose_name="Примечание",
        blank=True, null=True
    )
    delivery_price = models.DecimalField(
        max_digits=10, decimal_places=2,  # Две десятичные цифры
        verbose_name="Стоимость доставки",
        default=0, blank=True, null=True
    )
    discount_price = models.IntegerField(
        verbose_name="Скидка",
        default=0, blank=True, null=True
    )
    total_price = models.PositiveIntegerField(
        verbose_name="Итоговая сумма",
        default=0, blank=True, null=True
    )
    client_gave_money = models.IntegerField(
        verbose_name="Клиент дал денег",
        default=0, blank=True, null=True
    )
    change_price = models.IntegerField(
        verbose_name="Сдача клиенту",
        default=0, blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания биллинга"
    )

    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = self.generate_unique_payment_code()

        # Расчет объема товара
        if self.length_product and self.width_product and self.height_product:
            self.volume_product = self.length_product * self.width_product * self.height_product

        # Расчет стоимости доставки на основе веса и объема
        if self.weight_product and self.volume_product and self.volume_product > 0:
            rate_per_kg_m3 = 0.35
            self.delivery_price = round(self.weight_product / self.volume_product * rate_per_kg_m3, 2)
        else:
            self.delivery_price = 0

        # Учет скидок и сдачи
        self.total_price = max(0, self.delivery_price - self.discount_price)
        if self.client_gave_money:
            self.change_price = max(0, self.client_gave_money - self.total_price)

        super().save(*args, **kwargs)

    def generate_unique_payment_code(self):
        while True:
            payment_code = str(uuid.uuid4().int)[:10]
            if not Billing.objects.filter(payment_code=payment_code).exists():
                return payment_code

    class Meta:
        verbose_name = "Биллинг"
        verbose_name_plural = "Биллинги"

class BillingImage(models.Model):
    billing = models.ForeignKey(
        Billing, on_delete=models.CASCADE,
        related_name="billing_images", verbose_name="Биллинг"
    )
    image = models.ImageField(
        upload_to='billings_images/',
        verbose_name="Чек",
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время"
    )

    def __str__(self):
        return f"{self.billing} - {self.created}"
    
    class Meta:
        verbose_name = "Фотография биллинга"
        verbose_name_plural = "Фотографии биллинга"