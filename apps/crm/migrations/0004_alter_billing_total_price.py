# Generated by Django 5.0.6 on 2024-11-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_remove_billing_delivery_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30, null=True, verbose_name='Итоговая сумма'),
        ),
    ]
