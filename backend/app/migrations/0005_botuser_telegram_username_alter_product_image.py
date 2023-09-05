# Generated by Django 4.2.4 on 2023-09-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_product_subcategory_subcategory_name_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='telegram_username',
            field=models.CharField(blank=True, help_text='Enter username', max_length=150, null=True, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images', verbose_name='Image'),
        ),
    ]
