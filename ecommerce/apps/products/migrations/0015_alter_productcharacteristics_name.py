# Generated by Django 4.2 on 2023-05-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_products_bonuses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcharacteristics',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='characteristics name'),
        ),
    ]
