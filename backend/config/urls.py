
from django.contrib import admin
from django.urls import path, include

from config import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from app.views import set_language, index

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('set_language/<str:language>/', set_language, name='set-language'),
    path('', index, name='index'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('api/', include('app.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # ...
        path('__debug__/', include(debug_toolbar.urls)),
        # ...
    ]