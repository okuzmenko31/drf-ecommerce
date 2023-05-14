# Generated by Django 4.2 on 2023-04-12 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usertoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBonusesBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0, verbose_name='User balance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bonuses_balance', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]