from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters

from .serializers import *
from .models import *

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
    search_fields = ['name', ]

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


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
    def post(self):
        pass

