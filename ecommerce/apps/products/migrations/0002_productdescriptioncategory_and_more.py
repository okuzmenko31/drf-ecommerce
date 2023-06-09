# Generated by Django 4.2 on 2023-04-23 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDescriptionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Description category name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'Products descriptions categories',
            },
        ),
        migrations.AddField(
            model_name='productdescription',
            name='description_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productdescriptioncategory', verbose_name='Description category'),
        ),
    ]
