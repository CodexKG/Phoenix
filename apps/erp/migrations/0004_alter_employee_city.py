# Generated by Django 5.0.6 on 2024-10-31 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_alter_employee_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='city',
            field=models.ManyToManyField(blank=True, related_name='city_employees', to='erp.city', verbose_name='Город'),
        ),
    ]
