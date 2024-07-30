from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import home_page, header, footer, http_404
from Resume_shop import settings


urlpatterns = [
    path('', home_page),
    path('', include('accounts.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),
    path('', include('contacts.urls')),
    path('header', header, name='header'),
    path('footer', footer, name='footer'),
    path('404', http_404),
    path('admin/', admin.site.urls)
]


if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
