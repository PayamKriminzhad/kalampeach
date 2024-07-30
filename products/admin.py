from django.contrib import admin

from .models import Product, ProductGallery, Blog, BlogDetail, ProductComment, DiscountTimer, ProductAttr


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'price', 'active']
    list_editable = ['price', 'active']

    class Meta:
        model = Product

class ProductAttrAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'attr']
    list_editable = ['title', 'attr']

    class Meta:
        model = ProductAttr

class BlogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'active']
    list_editable = ['title', 'active']

    class Meta:
        model = Blog

class DiscountTimerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'time_end', 'active']
    list_editable = ['time_end', 'active']

    class Meta:
        model = DiscountTimer

admin.site.register(Product, ProductAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(DiscountTimer, DiscountTimerAdmin)
admin.site.register(ProductGallery)
admin.site.register(ProductComment)
admin.site.register(BlogDetail)
admin.site.register(ProductAttr, ProductAttrAdmin)