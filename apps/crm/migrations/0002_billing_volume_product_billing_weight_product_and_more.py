# Generated by Django 5.0.6 on 2024-11-02 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='volume_product',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Объем куб'),
        ),
        migrations.AddField(
            model_name='billing',
            name='weight_product',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Вес товара'),
        ),
        migrations.AlterField(
            model_name='billing',
            name='height_product',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Высота'),
        ),
        migrations.AlterField(
            model_name='billing',
            name='length_product',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Длина'),
        ),
        migrations.AlterField(
            model_name='billing',
            name='width_product',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Ширина'),
        ),
    ]