from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from products.models import Product
from .utils import unique_slug_generator


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, verbose_name='عنوان در url', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    products = models.ManyToManyField(Product, blank=True, verbose_name='محصولات')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'برچسب / تگ'
        verbose_name_plural = 'برچسب ها / تگ ها'


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f"{instance.title.replace(' ', '-')}"

pre_save.connect(tag_pre_save_receiver, sender=Tag)

# def tag_post_save_reciver(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.save()

# post_save.connect(tag_post_save_reciver, sender=Tag)
