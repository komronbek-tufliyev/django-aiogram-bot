from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'botuser', BotUserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'subcategory', SubCategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'order', OrderViewSet)
router.register(r'orderitem', OrderItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('set_language/<str:language>/', set_language, name='set-language'),
]



