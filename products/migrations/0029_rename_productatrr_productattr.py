# Generated by Django 4.1.5 on 2023-10-02 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_rename_productatrrs_productatrr'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductAtrr',
            new_name='ProductAttr',
        ),
    ]
