# Generated by Django 4.2 on 2023-05-05 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_address_order_city_order_email_order_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_info',
        ),
    ]
