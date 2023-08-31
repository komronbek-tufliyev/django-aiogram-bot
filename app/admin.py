from django.contrib import admin
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)

# Register your models here.
from .models import *
from .translation import CategoryTranslationOptions, ProductTranslationOptions
from modeltranslation.admin import TranslationAdmin

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'language')
    search_fields = ('name', 'telegram_id', 'language')
    list_filter = ('language', 'added')
    list_per_page = 10

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude')
    # search_fields = ('user', 'latitude', 'longitude')
    # list_filter = ('user', 'latitude', 'longitude')
    list_per_page = 10

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('picture', 'name', 'category', 'price', 'discount')
    search_fields = ('name', 'category', 'price', 'discount')
    list_filter = ('category', 'price', 'discount')
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'all_shop', 'all_products')
    list_per_page = 10

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'shop')
    list_per_page = 10

