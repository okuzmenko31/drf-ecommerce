# Generated by Django 4.2 on 2023-05-04 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_usershippinginfo_city_usershippinginfo_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershippinginfo',
            name='country',
        ),
    ]
