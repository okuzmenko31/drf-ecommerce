# Generated by Django 4.2 on 2023-05-15 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0003_usercoupons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercoupons',
            name='valid_to',
            field=models.DateField(blank=True, null=True, verbose_name='Coupon valid to'),
        ),
    ]
