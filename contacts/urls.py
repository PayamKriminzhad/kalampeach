from django.urls import path, include

from .views import contact_us

urlpatterns = [
    path('contact-us', contact_us),
]