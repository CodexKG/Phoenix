# Generated by Django 5.0.6 on 2024-11-02 10:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_type', models.CharField(choices=[('Лидогенерация', 'Лидогенерация'), ('Биллинг', 'Биллинг')], default='Лидогенерация', max_length=100, verbose_name='Тип биллинга')),
                ('billing_receipt_type', models.CharField(choices=[('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка'), ('Неизвестно', 'Неизвестно')], default='Неизвестно', max_length=100, verbose_name='Вид получения товара')),
                ('billing_status', models.CharField(choices=[('В корзине', 'В корзине'), ('Оформлен', 'Оформлен'), ('Оплачен', 'Оплачен'), ('Доставлен', 'Доставлен'), ('Возврат', 'Возврат'), ('Неизвестно', 'Неизвестно')], default='В корзине', max_length=100, verbose_name='Статус заказа')),
                ('billing_payment_status', models.CharField(choices=[('Оплачен', 'Оплачен'), ('Не оплачен', 'Не оплачен'), ('Ошибка', 'Ошибка'), ('В исполнении', 'В исполнении')], default='В исполнении', max_length=100, verbose_name='Статус оплаты')),
                ('billing_payment', models.CharField(choices=[('Наличными в магазине', 'Наличными в магазине'), ('Наличными курьеру', 'Наличными курьеру'), ('Оплата картой курьеру', 'Оплата картой курьеру'), ('Оплата начислением', 'Оплата начислением'), ('Оплата в рассрочку', 'Оплата в рассрочку'), ('Картой Visa', 'Картой Visa'), ('Мбанк', 'Мбанк'), ('Optima 24', 'Optima 24'), ('О! Деньги', 'О! Деньги'), ('Bakai 24', 'Bakai 24'), ('Ошибка', 'Ошибка'), ('Неизвестно', 'Неизвестно')], default='Неизвестно', max_length=100, verbose_name='Способы оплаты')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефонный номер')),
                ('payment_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Код оплаты')),
                ('delivery_from', models.CharField(blank=True, max_length=250, null=True, verbose_name='Доставка откуда')),
                ('delivery_to', models.CharField(blank=True, max_length=250, null=True, verbose_name='Доставка куда')),
                ('type_product', models.CharField(blank=True, max_length=500, null=True, verbose_name='Вид товара')),
                ('length_product', models.CharField(blank=True, max_length=255, null=True, verbose_name='Длина')),
                ('width_product', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ширина')),
                ('height_product', models.CharField(blank=True, max_length=255, null=True, verbose_name='Высота')),
                ('country', models.CharField(blank=True, default='Кыргызстан', max_length=255, null=True, verbose_name='Страна')),
                ('region', models.CharField(blank=True, max_length=255, null=True, verbose_name='Регион')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('apartment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Квартира')),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Индекс')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('delivery_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Стоимость доставки')),
                ('discount_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='Скидка')),
                ('delivery_date_time', models.DateTimeField(blank=True, null=True, verbose_name='Дата время доставки')),
                ('client_gave_money', models.IntegerField(blank=True, default=0, null=True, verbose_name='Клиент дал денег')),
                ('change_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='Сдача клиенту')),
                ('total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Итоговая сумма')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания биллинга')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Биллинг',
                'verbose_name_plural': 'Биллинги',
            },
        ),
        migrations.CreateModel(
            name='BillingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='billings_images/', verbose_name='Чек')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_images', to='crm.billing', verbose_name='Биллинг')),
            ],
            options={
                'verbose_name': 'Фотография биллинга',
                'verbose_name_plural': 'Фотографии биллинга',
            },
        ),
    ]