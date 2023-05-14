# Generated by Django 4.2 on 2023-05-04 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_products_availability_status'),
        ('orders', '0003_order_delivery_method_alter_order_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('total_price', models.IntegerField(default=0, verbose_name='Total price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'Items in order',
                'ordering': ['total_price'],
            },
        ),
    ]