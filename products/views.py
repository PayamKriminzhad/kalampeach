from genericpath import exists
import itertools
from django import http
from django.shortcuts import redirect, render
from django.http import Http404
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth import authenticate
import datetime
from django.contrib import messages

from .forms import CommentForm, CommentFormLogged
from .models import Product, ProductAttr, ProductManager, ProductGallery, ProductComment, Blog
from categories.models import Category
from orders.forms import UserNewOrderForm, UserNewOrderFormForComponent, UserLikeForm
from accounts.models import Dashbord
from dynamics.models import SiteSetting

class ProductList(ListView):
    template_name = 'products_list.html'
    paginate_by = 8

    def get_queryset(self):
        price_range = self.request.GET.get('f')
        products = Product.objects.get_active_products()
        if price_range is not None:
            result = [int(x) for x in price_range.split() if x.isdigit()]
            return products.filter(price_discount__range=(result[1], result[0]))
        return products



class ProductListByCategory(ListView):
    template_name = 'products_list.html'
    paginate_by = 8

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        price_range = self.request.GET.get('f')
        category = Category.objects.filter(name__iexact=category_name)
        if category is None:
            return redirect('/404')
        products_by_category = Product.objects.get_products_by_category(category_name)
        if price_range is not None:
            result = [int(x) for x in price_range.split() if x.isdigit()]
            return products_by_category.filter(price_discount__range=(result[1], result[0]))
        return Product.objects.get_products_by_category(category_name)

class ProductSearch(ListView):
    template_name = 'products_list.html'
    paginate_by = 8

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        price_range = request.GET.get('f')
        if query is not None:
            products = Product.objects.search(query).distinct()
            if price_range is not None:
                result = [int(x) for x in price_range.split() if x.isdigit()]
                return products.filter(price_discount__range=(result[1], result[0]))
            return Product.objects.search(query).distinct()
        return Product.objects.get_active_products().distinct()

class ProductFilter(ListView):
    template_name = 'products_list.html'
    paginate_by = 8
    
    def get_queryset(self):
        request = self.request
        price = request.GET.get('f')
        result = [int(x) for x in price.split() if x.isdigit()]
        if result is not None:
            return Product.objects.filter(price_discount__range=(result[1], result[0]))
        return Product.objects.get_active_products()

def price_range_partial(request, url):
    value = request.GET.get('f')

    context = {
        'value' : value,
        'url' : url
    }
    return render(request, 'price_range.html', context)

def products_categories_partial(request, url):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'url' : url
    }
    return render(request, 'products_categories_partial.html', context)

def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, *args, **kwargs):
    if request.user.is_authenticated:
        user = request.user
        dashboard = Dashbord.objects.filter(owner_id=user.id).first()

    productId = kwargs['productId']
    product = Product.objects.get_by_id(productId)

    if product is None or not product.active:
        return redirect('/404')

    category_name = product.categories.first()
    related_products = Product.objects.filter(~Q(id=productId), categories__product=product).distinct()[:4]

    order_form = UserNewOrderForm(request.POST or None, initial={'product_id':productId})

    gallery = ProductGallery.objects.filter(product_id=productId)
    grouped_gallery = list(my_grouper(3, gallery))

    attrs = ProductAttr.objects.filter(product_id=productId)

    if not request.user.is_authenticated:
        comment_form = CommentForm(request.POST or None, initial={'product_id':productId, 'date':datetime.date.today()})
        if comment_form.is_valid():
            name = comment_form.cleaned_data.get('name')
            email = comment_form.cleaned_data.get('email')
            massage = comment_form.cleaned_data.get('massage')
            date = comment_form.cleaned_data.get('date')
            rate = comment_form.cleaned_data.get('rate')
            motherID = comment_form.cleaned_data.get('product_id')

            ProductComment.objects.create(product_id=motherID, name=name, email=email, massage=massage, date=date, rate=rate)
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            # return redirect(f'{product.get_absolute_url()}')
    
    if request.user.is_authenticated:
        if user.get_full_name() is None:
            name_for_comment = user.get_full_name()
        else:
            name_for_comment = user.username
        comment_form = CommentFormLogged(request.POST or None, initial={'product_id':productId, 'profile':dashboard.profile, 'name':name_for_comment, 'email':user.email, 'date':datetime.date.today()})
        if comment_form.is_valid():
            name = comment_form.cleaned_data.get('name')
            email = comment_form.cleaned_data.get('email')
            massage = comment_form.cleaned_data.get('massage')
            date = comment_form.cleaned_data.get('date')
            rate = comment_form.cleaned_data.get('rate')
            motherID = comment_form.cleaned_data.get('product_id')

            ProductComment.objects.create(product_id=motherID, profile=dashboard.profile, name=name, email=email, massage=massage, date=date, rate=rate)
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            # return redirect(f'{product.get_absolute_url()}')
    comments = product.productcomment_set.all()
    product_rate = product.get_average_rate()

    like_form = UserLikeForm(request.POST or None, initial={'product':product.id})

    context = {
        'product': product,
        'gallery': grouped_gallery,
        'related': related_products,
        'category': category_name,
        'orderform':order_form,
        'commentform':comment_form,
        'comments':comments,
        'liked':False,
        'like_form':like_form,
        'attrs':attrs,
        'range':range(5),
        'range_product_rate_1': range(product_rate),
        'range_product_rate_2': range(5 - product_rate)
    }
    if request.user.is_authenticated:
        liked = dashboard.liked.filter(product_id=product.id).first()
        if liked is not None:
            context['liked'] = True

    return render(request, 'product_detail.html', context)

def product_component(request, product):
    order_form = UserNewOrderFormForComponent(request.POST or None, initial={'product_id':product.id, 'count':1})
    like_form = UserLikeForm(request.POST or None, initial={'product':product.id})

    context ={
        'product': product,
        'form':order_form,
        'like_form':like_form,
        'is_liked': False,
        'is_new': False
    }
    if request.user.is_authenticated:
        user_id = request.user.id
        dashbord = Dashbord.objects.filter(owner_id=user_id).first()
        liked = dashbord.liked.filter(product_id=product.id).first()
        if liked is not None:
            context['is_liked'] = True

    latest_products = Product.objects.order_by('-id').all()[:8]
    if product in latest_products:
        context['is_new'] = True

    return render(request, 'product_item_component.html', context)



def blog(request, *args, **kwargs):

    blogId = kwargs['blogId']
    blog = Blog.objects.get(id=blogId)

    if blog is None or not blog.active:
        return redirect('/404')

    blog_details = blog.blogdetail_set.all()

    context ={
        'blog': blog,
        'pages': blog_details
    }
    return render(request, 'blog.html', context)
