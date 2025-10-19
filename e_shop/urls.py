from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls')),
    path('', RedirectView.as_view(url='/', permanent=False)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root = settings.MEDIA_ROOT)