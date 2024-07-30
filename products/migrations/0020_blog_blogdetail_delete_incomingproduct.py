# Generated by Django 4.1.5 on 2023-05-06 08:30

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_productcomment_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.models.upload_image_path_blog, verbose_name='تصویر')),
                ('active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'بلاگ',
                'verbose_name_plural': 'بلاگ ها',
            },
        ),
        migrations.CreateModel(
            name='BlogDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.models.upload_image_path_blog_detail, verbose_name='تصویر')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.blog', verbose_name='بلاگ')),
            ],
            options={
                'verbose_name': 'صفحه بلاگ',
                'verbose_name_plural': 'صفحات بلاگ',
            },
        ),
        migrations.DeleteModel(
            name='IncomingProduct',
        ),
    ]
