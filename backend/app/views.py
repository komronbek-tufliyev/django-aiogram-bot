from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
# from django_filters import rest_framework as filters

from .serializers import *
from .models import *
from django.db.models import Prefetch

def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class BotUserViewSet(viewsets.ModelViewSet):
    serializer_class = BotUserSerializer
    queryset = BotUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'subcategories__name', 'name_uz', 'subcategories__name_uz', 'name_ru', 'subcategories__name_ru', 'name_en', 'subcategories__name_en']

    # def filter_queryset(self, queryset):
    #     return super().filter_queryset(queryset).prefetch_related('subcategories')
    
    # def get_queryset(self):
    #     queryset = Category.objects.all()
    #     category = self.request.query_params.get('q', None)
    #     if category is not None:
    #         queryset = queryset.filter(category=category)
    #     return queryset
    

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category__name', 'name_uz', 'category__name_uz', 'name_ru', 'category__name_ru', 'name_en', 'category__name_en']

    def filter_queryset(self, queryset):
        # SubCategory.refresh_from_db()
        term = self.request.query_params.get('search', None)
        print(term)
        print(SubCategory.objects.all())
        result = SubCategory.objects.filter(category__name__contains=term)
        print(result)
        return result

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'about' ]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


from rest_framework.views import APIView

class ChangeLanguage(APIView):
    def post(self, request):
        if not request.method == 'POST':
            return Response({'status': 'Method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        data = request.data
        telegram_id = data.get('telegram_id', None)
        
        try:
            user = BotUser.objects.get(telegram_id=telegram_id)
        except BotUser.DoesNotExist:
            return Response({'status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.language = data.get('language', user.language)
        user.save()
        return Response({'status': 'Language changed!'})
    
class ChangePhoneNumber(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        telegram_id = data.get('telegram_id')
        user = BotUser.objects.get(telegram_id=telegram_id)
        user.phone = data.get('phone')
        user.save()
        return Response({'status': 'Phone number changed!'})
    
class OrderItems(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        telegram_id = data.get('telegram_id')
        user = BotUser.objects.get(telegram_id=telegram_id)
        order = Order.objects.filter(user=user)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     data = request.POST
    #     data = data.dict()
    #     telegram_id = data.get('telegram_id')
        
    #     user = BotUser.objects.prefetch_related(
    #         Prefetch('order_set', queryset=Order.objects.select_related('user'))
    #     ).get(telegram_id=telegram_id)
        
    #     orders = user.order_set.all()
    #     serializer = OrderSerializer(orders, many=True)
        
    #     return Response(serializer.data)

class SetOrderItem(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()

        telegram_id = data.get('telegram_id')
        product = data.get('product')
        quantity = data.get('quantity')
        user = BotUser.objects.get(telegram_id=telegram_id)
        product = Product.objects.get(id=product)
        order, created = Order.objects.get_or_create(user=user)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if int(quantity) > 0:
            order_item.quantity = quantity
            order_item.save()
            return Response({'status': 'Order item updated!'})
        else:
            order_item.delete()
            return Response({'status': 'Order item deleted!'})


class DestroyBasket(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        telegram_id = data.get('telegram_id')
        user = BotUser.objects.get(telegram_id=telegram_id)
        try:
            order = Order.objects.get(user=user)
            order.delete()
        except Order.DoesNotExist:
            pass
        except Exception as e:
            print(e)
            pass
        return Response({'status': 'Basket deleted!'})
    
class BotUserInfo(APIView):
    def post(self, request):
        data = request.data
        botuser = BotUser.objects.get(telegram_id=data.get('telegram_id'))
        serializer = BotUserSerializer(instance=botuser, partial=True)
        return Response(serializer.data)

class DeleteItem(APIView):
    def post(self, request):
        data = request.data
        data = data.dict()

        telegram_id = data.get('telegram_id')
        product = data.get('product')
        user = BotUser.objects.get(telegram_id=telegram_id)
        product = Product.objects.get(id=product)
        order, created = Order.objects.get_or_create(user=user)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.delete()
        return Response({'status': 'Order item deleted!'})



