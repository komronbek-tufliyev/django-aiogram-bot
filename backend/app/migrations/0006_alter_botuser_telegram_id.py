# Generated by Django 4.2.4 on 2023-09-06 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_botuser_telegram_username_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botuser',
            name='telegram_id',
            field=models.IntegerField(db_index=True, help_text='Enter Telegram ID', unique=True, verbose_name='Telegram ID'),
        ),
    ]