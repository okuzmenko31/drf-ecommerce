# Generated by Django 4.2 on 2023-04-23 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_alter_category_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCharacteristicsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'Characteristics category',
            },
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'description',
                'verbose_name_plural': 'Descriptions',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350, verbose_name='Name')),
                ('price', models.IntegerField(default=0, verbose_name='Price')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/products/', verbose_name='Photo')),
                ('discount', models.IntegerField(default=0, verbose_name='Discount(Optional)')),
                ('article', models.CharField(blank=True, max_length=8, verbose_name='Article')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='Rating')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='categories.category', verbose_name='Category')),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productdescription', verbose_name='Description')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/products/all/', verbose_name='Product photos')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='products.products', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True, verbose_name='characteristics name')),
                ('value', models.CharField(max_length=200, verbose_name='Value')),
                ('characteristics_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='products.productcharacteristicscategory', verbose_name='Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='products.products', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'description',
                'verbose_name_plural': 'Descriptions',
            },
        ),
    ]
