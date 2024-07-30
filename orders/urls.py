from django.urls import path

from .views import add_user_order, open_user_order, remove_order_detail, add_user_like, remove_user_like, confirm, send_request, verify

urlpatterns = [
    path('add-user-order', add_user_order),
    path('add-user-like', add_user_like),
    path('remove-user-like', remove_user_like),
    path('open-order', open_user_order),
    path('remove-order-detail/<detail_id>', remove_order_detail),
    path('confirm', confirm),
    path('request', send_request, name='request'),
    path('verify/<order_id>', verify, name='verify')
]
