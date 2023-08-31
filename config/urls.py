
from django.contrib import admin
from django.urls import path, include

from config import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
# from app.views import set_language

urlpatterns = [
    path('kal/', include('app.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    # path('set_language/<str:language>/', set_language, name='set-language'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
