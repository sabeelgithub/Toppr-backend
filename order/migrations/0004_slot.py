# Generated by Django 4.2.1 on 2023-06-22 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_client_wallet'),
        ('order', '0003_subscription_terminated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('day', models.DateField(auto_now=True)),
                ('booked', models.BooleanField(default=False)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.expert')),
            ],
        ),
    ]
