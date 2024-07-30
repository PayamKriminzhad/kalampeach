# from turtle import title
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    email = models.EmailField(max_length=80, verbose_name='ایمیل')
    title = models.CharField(max_length=150, verbose_name='موضوع')
    massage = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.title