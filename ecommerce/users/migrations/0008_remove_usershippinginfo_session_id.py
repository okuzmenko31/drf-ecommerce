# Generated by Django 4.2 on 2023-05-05 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_usershippinginfo_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershippinginfo',
            name='session_id',
        ),
    ]
