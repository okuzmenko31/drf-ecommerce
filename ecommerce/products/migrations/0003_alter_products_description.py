# Generated by Django 4.2 on 2023-04-23 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productdescriptioncategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productdescription', verbose_name='Description'),
        ),
    ]
