from django.urls import path, include

from .views import ProductList, product_detail, ProductSearch, ProductListByCategory, ProductFilter, products_categories_partial, blog

urlpatterns = [
    path('products', ProductList.as_view()),
    path('products/<productId>/<name>', product_detail),
    path('products/search', ProductSearch.as_view()),
    path('products/range', ProductFilter.as_view()),
    path('products/<category_name>', ProductListByCategory.as_view()),
    path('blogs/<blogId>/<name>', blog),
]