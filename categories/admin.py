from pyexpat import model
from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'name']
    list_editable = ['name']
    
    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)