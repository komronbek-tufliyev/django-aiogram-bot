# Generated by Django 4.2.4 on 2023-08-31 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botuser',
            name='language',
            field=models.CharField(default='uz', max_length=5, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uz',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Category'),
        ),
    ]
