# Generated by Django 4.1.5 on 2023-01-26 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='categories.category', verbose_name='دسته بندی ها'),
        ),
    ]
