# Generated by Django 4.2 on 2023-05-15 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
    ]
