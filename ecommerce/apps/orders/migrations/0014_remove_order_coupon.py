# Generated by Django 4.2 on 2023-05-16 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_remove_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
    ]
