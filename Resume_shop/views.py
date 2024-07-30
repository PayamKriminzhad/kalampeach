from pickle import TRUE
from django.shortcuts import render

from products.models import Blog, Product, DiscountTimer
from dynamics.models import SiteSetting
from orders.models import Order


def header(request):
    setting = SiteSetting.objects.first()
    context = {
        'setting':setting
    }

    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(is_paid=False, owner_id=user.id).first()
        context['user'] = user
        context['order'] = order

    return render(request, 'shared/Header.html', context)

def footer_rules(request):
    setting = SiteSetting.objects.first()
    context = {
        'setting':setting
    }
    return render(request, 'shared/Footer_rules.html', context)

def footer(request):
    setting = SiteSetting.objects.first()

    context = {
        'setting':setting
    }

    return render(request, 'shared/Footer.html', context)

def home_page(request):

    blog = Blog.objects.filter(active=True)
    setting = SiteSetting.objects.first()

    categories = setting.category_set.all()

    latest_products = Product.objects.order_by('-id').filter(active=True)[:8]

    most_visited = Product.objects.order_by('-visit_count').filter(active=True)[:8]

    timer = DiscountTimer.objects.all()

    context = {
        'blog':blog,
        'setting':setting,
        'categories':categories,
        'latest':latest_products,
        'visited':most_visited,
        'timer':timer
    }
    return render(request, 'home_page.html', context)


def http_404(request):

    context = {}

    return render(request, '404.html', context)