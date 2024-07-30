import os

from django.db import models


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"logo-image/{final_name}"
    

def upload_categoryimage_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.category}{ext}"
    return f"categories/{final_name}"



class SiteSetting(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان سایت', null=True, blank=True)
    slidersentence_home = models.CharField(max_length=150, verbose_name='جمله اسلایدر/ صفحه اصلی', null=True, blank=True)
    sliderdate_home = models.CharField(max_length=150, verbose_name='تاریخ اسلایدر/ صفحه اصلی', null=True, blank=True)
    sliderimage_home = models.ImageField(verbose_name='عکس اسلایدر/ صفحه اصلی', null=True, blank=True)
    firstsentence_contact = models.CharField(max_length=150, verbose_name='جمله اول/ ارتباط با ما', null=True, blank=True)
    address_contact = models.CharField(max_length=400, verbose_name='آدرس/ ارتباط با ما', null=True, blank=True)
    phone_contact = models.CharField(max_length=50, verbose_name='تلفن/ ارتباط با ما', null=True, blank=True)
    mobile_contact = models.CharField(max_length=50, verbose_name='تلفن همراه/ ارتباط با ما', null=True, blank=True)
    openhours_contact = models.CharField(max_length=400, verbose_name='ساعات باز/ ارتباط با ما', null=True, blank=True)
    email_contact = models.EmailField(max_length=50, verbose_name='ایمیل/ ارتباط با ما', null=True, blank=True)
    footerrules1a = models.CharField(max_length=150, verbose_name='1aقوانین پاورقی', null=True, blank=True)
    footerrules1b = models.CharField(max_length=150, verbose_name='1bقوانین پاورقی', null=True, blank=True)
    footerrules2a = models.CharField(max_length=150, verbose_name='2aقوانین پاورقی', null=True, blank=True)
    footerrules2b = models.CharField(max_length=150, verbose_name='2bقوانین پاورقی', null=True, blank=True)
    footerrules3a = models.CharField(max_length=150, verbose_name='3aقوانین پاورقی', null=True, blank=True)
    footerrules3b = models.CharField(max_length=150, verbose_name='3bقوانین پاورقی', null=True, blank=True)
    footerrules4a = models.CharField(max_length=150, verbose_name='4aقوانین پاورقی', null=True, blank=True)
    footerrules4b = models.CharField(max_length=150, verbose_name='4bقوانین پاورقی', null=True, blank=True)
    copy_right = models.CharField(verbose_name='متن کپی رایت', null=True, blank=True, max_length=200)
    logo_image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر لوگو')
    maps = models.CharField(max_length=250, verbose_name='گوگل مپ', blank=True)
    instagram = models.CharField(max_length=250, verbose_name='اینستاگرام', blank=True)
    telegram = models.CharField(max_length=250, verbose_name='توییتر', blank=True)
    whatsapp = models.CharField(max_length=250, verbose_name='واتساپ', blank=True)


    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'مدیریت تنظیمات'

    def __str__(self):
        return self.title


class Category(models.Model):
    mother = models.ForeignKey(SiteSetting, on_delete=models.CASCADE)
    category = models.CharField(max_length=150, verbose_name='دسته بندی')
    ref = models.CharField(max_length=150, verbose_name='آدرس')
    image = models.ImageField(upload_to=upload_categoryimage_path, null=True, blank=True, verbose_name='تصویر')
    

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.category
