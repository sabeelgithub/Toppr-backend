# Generated by Django 4.2.1 on 2023-06-24 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_slot_expired'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='expired',
        ),
    ]