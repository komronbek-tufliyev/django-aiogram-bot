from rest_framework import serializers
from .models import *

class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = '__all__'
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = '__all__'        

class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    shop = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)
    
    def get_shop(self, obj):
        return obj.shop
    
    def get_product_id(self, obj):
        return obj.product_id

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product', 'quantity', 'shop']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    products_count = serializers.SerializerMethodField(read_only=True)
    all_shop = serializers.SerializerMethodField(read_only=True)

    def get_product_count(self, obj):
        return obj.all_products
    
    def get_all_shop(self, obj):
        return obj.all_shop
    
    class Meta:
        model = Order
        fields = ['id', 'items', 'created', 'products_count', 'all_shop']


