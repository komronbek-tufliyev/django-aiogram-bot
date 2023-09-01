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

    path('change/', ChangeLanguage.as_view(), name='change-language'),
    path('phone/', ChangePhoneNumber.as_view(), name='change-phone'),
    path('shop/', OrderItems.as_view(), name='order-items'),
    path('set_order/', SetOrderItem.as_view(), name='set-order'),
    path('delete_basket', DestroyBasket.as_view(), name='delete-basket'),
    path('user/', BotUserInfo.as_view(), name='user'),
    path('delete_item/', DeleteItem.as_view(), name='delete-item'),
]



