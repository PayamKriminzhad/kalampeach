from django.contrib import admin

from .models import SiteSetting, Category

admin.site.register(SiteSetting)
admin.site.register(Category)
