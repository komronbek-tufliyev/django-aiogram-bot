from import_export.resources import ModelResource
from .models import Category, Product, SubCategory

class CategoryResource(ModelResource):
    class Meta:
        model = Category

class SubCategoryResource(ModelResource):
    class Meta:
        model = SubCategory

class ProductResource(ModelResource):
    class Meta:
        model = Product
    
