# Generated by Django 4.2.1 on 2023-06-07 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0002_domain_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tutorial',
            unique_together={('tutorial_name', 'domain')},
        ),
    ]
