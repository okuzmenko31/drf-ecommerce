# Generated by Django 4.2 on 2023-05-05 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_usershippinginfo_session_id'),
        ('orders', '0008_order_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='patronymic',
        ),
        migrations.RemoveField(
            model_name='order',
            name='post_office',
        ),
        migrations.RemoveField(
            model_name='order',
            name='surname',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.usershippinginfo', verbose_name='User shipping info'),
        ),
    ]