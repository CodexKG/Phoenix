# Generated by Django 5.0.6 on 2024-11-10 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0003_alter_card_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='attachments',
        ),
    ]