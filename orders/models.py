from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name='پرداخت شده / نشده')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
    cellphone = models.CharField(max_length=50, verbose_name='تلفن همراه', null=True, blank=True)
    homephone = models.CharField(max_length=50, verbose_name='تلفن ثابت', null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='آدرس ارسال', null=True, blank=True)
    is_delivered = models.BooleanField(max_length=50, verbose_name='فرستاده شده', default=False)

    def get_total_price(self):
        total = 0
        for i in self.orderdetail_set.all():
            total += i.get_price()
        return total

    def __str__(self):
        return self.owner.get_full_name()
    
    def get_detailcount(self):
        count = 0
        for i in self.orderdetail_set.all():
            count+=1
        return count

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    count = models.IntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'جزییات محصول'
        verbose_name_plural = 'اطلاعات جزییات محصولات'

    def get_price(self):
        return self.count * self.product.final_price()

    def __str__(self):
        return self.product.title

