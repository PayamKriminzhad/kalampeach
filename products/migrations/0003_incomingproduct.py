# Generated by Django 4.1.5 on 2023-01-27 06:55

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('products', '0002_product_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('categories', models.ManyToManyField(blank=True, to='categories.category', verbose_name='دسته بندی ها')),
            ],
            options={
                'verbose_name': 'محصول در راه',
                'verbose_name_plural': 'محصولات در راه',
            },
        ),
    ]
