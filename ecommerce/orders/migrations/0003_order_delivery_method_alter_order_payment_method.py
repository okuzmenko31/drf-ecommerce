# Generated by Django 4.2 on 2023-05-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_activate_bonuses_order_create_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_method',
            field=models.IntegerField(choices=[(1, 'Courier'), (2, 'To the post office')], default=2, verbose_name='Delivery method'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'By cash'), (2, 'By card')], default=1, verbose_name='Payment method'),
        ),
    ]
