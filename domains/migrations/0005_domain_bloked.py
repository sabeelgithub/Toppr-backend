# Generated by Django 4.2.1 on 2023-06-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0004_alter_sub_tutorial_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='bloked',
            field=models.BooleanField(default=False),
        ),
    ]
