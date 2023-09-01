# Generated by Django 4.2.4 on 2023-08-31 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter name', max_length=150, null=True, verbose_name='Name')),
                ('telegram_id', models.CharField(max_length=20, unique=True, verbose_name='Telegram ID')),
                ('language', models.CharField(default='uz', max_length=5, verbose_name='Language)')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'BotUser',
                'verbose_name_plural': 'BotUsers',
                'db_table': 'BotUser',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Category)')),
                ('name_uz', models.CharField(blank=True, max_length=150, null=True, verbose_name='Category)')),
                ('name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='Category)')),
                ('name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='Category)')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.botuser', to_field='telegram_id', verbose_name='Bot User')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('name_uz', models.CharField(max_length=150, null=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=150, null=True, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=150, null=True, verbose_name='Name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product-images', verbose_name='Image')),
                ('about', models.TextField(blank=True, null=True, verbose_name='Info')),
                ('about_uz', models.TextField(blank=True, null=True, verbose_name='Info')),
                ('about_en', models.TextField(blank=True, null=True, verbose_name='Info')),
                ('about_ru', models.TextField(blank=True, null=True, verbose_name='Info')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Discount')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app.product', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, max_length=50, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, max_length=50, null=True, verbose_name='Longitude')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.botuser', to_field='telegram_id', verbose_name='Bot User')),
            ],
        ),
    ]