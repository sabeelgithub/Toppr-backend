# Generated by Django 4.2.1 on 2023-06-08 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0003_alter_tutorial_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sub_tutorial',
            unique_together={('sub_tutorial_name', 'tutorial')},
        ),
    ]