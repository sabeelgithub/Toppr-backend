# Generated by Django 4.2.1 on 2023-06-20 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_subscription_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='terminated',
            field=models.BooleanField(default=False, null=True),
        ),
    ]