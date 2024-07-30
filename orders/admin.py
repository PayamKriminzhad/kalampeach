from django.contrib import admin
from .models import Order, OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'payment_date', 'is_paid', 'is_delivered']
    list_editable = ['is_paid', 'is_delivered']

    class Meta:
        model = Order



class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'count']
    list_editable = []

    class Meta:
        model = OrderDetail

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)