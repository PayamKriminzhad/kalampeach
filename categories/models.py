from django.db import models
from django.db.models.signals import pre_save, post_save


class Category(models.Model):

    title = models.CharField(max_length=150, verbose_name='عنوان')
    name = models.SlugField(max_length=150, verbose_name='عنوان در URL', blank=True)
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

    def get_url(self):
        return f"http://127.0.0.1:8000/products/{self.name}"

def get_slug(sender, instance, *args, **kwargs):
    if not instance.name:
        instance.name = f"{instance.title.replace(' ', '-')}"

pre_save.connect(get_slug, sender=Category)
