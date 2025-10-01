from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available']
    prepopulated_fields = {'slug': ('name',)}

    list_editable = ['price', 'available']

    search_fields = ['name','description']
    list_filter = ['category', 'available', 'updated', 'created']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
