# Generated by Django 5.0.6 on 2024-09-21 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ('position',), 'verbose_name': 'Карточка', 'verbose_name_plural': 'Карточки'},
        ),
    ]
