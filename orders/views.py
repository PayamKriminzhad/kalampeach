import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from zeep import Client
from django.contrib import messages
from kavenegar import *

from accounts.models import Dashbord
from .forms import UserNewOrderForm, UserLikeForm, OrderConfirmForm
from .models import Order, OrderDetail
from products.models import Product


def payamak(phone, message):
    api = KavenegarAPI('546A3571462F4D6C4744782F52302B487275453538476C5978557032316C386B614B4F5865702B354352673D')
    params = { 'sender' : '10008663', 'receptor': phone, 'message' : message }
    response = api.sms_send(params)

@login_required(login_url='/login')
def add_user_order(request):
    new_order = UserNewOrderForm(request.POST or None)
    if new_order.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()

        if order is None:
            order=Order.objects.create(owner_id=request.user.id, is_paid=False)

        product_id = new_order.cleaned_data.get('product_id')
        count = new_order.cleaned_data.get('count')
        if count < 1 :
            count = 1

        product = Product.objects.get_by_id(product_id)
        if count > product.store:
            messages.error(request, f'این کالا به تعداد مورد نظر موجود نیست. موجودی: {product.store}')
            return redirect(product.get_absolute_url())
        if_product_exists: OrderDetail = order.orderdetail_set.filter(product_id=product_id).first()
        if if_product_exists is not None:
            if_product_exists.count += count
            if_product_exists.save()
        else:
            order.orderdetail_set.create(product_id=product_id, count=count)
        
        messages.success(request, 'این محصول به سبد خرید شما اضافه شد')
        return redirect(f'{product.get_absolute_url()}')
    return redirect('/')


@login_required(login_url='/login')
def add_user_like(request):
    like_form = UserLikeForm(request.POST or None)
    dashbord = Dashbord.objects.filter(owner_id=request.user.id).first()

    if like_form.is_valid():
        product_id = like_form.cleaned_data.get('product')
        dashbord.liked.create(product_id=product_id)
        product = Product.objects.get_by_id(product_id)

        messages.success(request, 'این محصول در قسمت مورد علاقه های شما ثبت شد')
        return redirect(f'{product.get_absolute_url()}')


@login_required(login_url='/login')
def remove_user_like(request):
    like_form = UserLikeForm(request.POST or None)
    dashbord = Dashbord.objects.filter(owner_id=request.user.id).first()
    
    if like_form.is_valid():
        product_id = like_form.cleaned_data.get('product')
        dislike = dashbord.liked.get(product_id=product_id)
        dislike.delete()
        product = Product.objects.get_by_id(product_id)

        messages.success(request, 'این محصول از قسمت مورد علاقه های شما حذف شد')
        return redirect(f'{product.get_absolute_url()}')



@login_required(login_url='/login')
def open_user_order(request):

    context = {
        'order':None,
        'detail':None,
        'total':0
    }

    order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if order is not None:
        context['order'] = order
        context['details'] = order.orderdetail_set.all()
        context['total'] = order.get_total_price

    return render(request, 'cart.html', context)


@login_required(login_url='/login')
def remove_order_detail(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
            return redirect('/open-order')
    return redirect('/404')



MERCHANT = '1ba406b1-8add-434b-be7d-03549863be10'
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for realy server.

def send_request(request, *args, **kwargs):
    total_price = 0
    open_order: Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    if open_order is not None and open_order.get_total_price() > 0:
        total_price = open_order.get_total_price()
        result = client.service.PaymentRequest(
            MERCHANT, total_price, description, email, mobile, f"{CallbackURL}/{open_order.id}"
        )
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    return redirect('/404')


def verify(request, *args, **kwargs):
    order_id = kwargs.get('order_id')
    user_order = Order.objects.get_queryset().get(id=order_id)
    total_price = user_order.get_total_price()
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], total_price)
        if result.Status == 100:
            user_order = Order.objects.get_queryset().get(id=order_id)
            user_order.is_paid = True
            user_order.payment_date = datetime.date.today()
            user_order.save()
            for detail in user_order.orderdetail_set.all():
                detail.product.store = detail.product.store - detail.count
                detail.product.save()
            payamak(user_order.cellphone, f"ممنون که ما رو انتخاب کردید:)\nکد سفارش شما:\n\n {user_order.payment_date.strftime('%Y%m%d')}{user_order.cellphone[-4:]}\n\n کلم پیچ")
            messages.success(request, f"سفارش شما با موفقیت ثبت شد. کد سفارش: {user_order.payment_date.strftime('%Y%m%d')}{user_order.cellphone[-4:]}")
            return redirect("/open-order")
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')

@login_required(login_url='/login')
def confirm(request):

    order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    dashbord = Dashbord.objects.filter(owner_id=request.user.id).first()
    
    confirm_form = OrderConfirmForm(request.POST or None, initial={'cellphone': dashbord.ph_number, 'address':dashbord.address})
    if confirm_form.is_valid():
        cellphone = confirm_form.cleaned_data.get('cellphone')
        homephone = confirm_form.cleaned_data.get('homephone')
        address = confirm_form.cleaned_data.get('address')
        order.cellphone = cellphone
        order.homephone = homephone
        order.address = address
        order.save()
        return redirect('/request')


    context = {
        'form':confirm_form,
    }
    return render(request, 'confirm.html', context)