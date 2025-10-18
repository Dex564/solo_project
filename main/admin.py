from django.contrib import admin
from .models import Product, Category, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available']
    prepopulated_fields = {'slug': ('name',)}

    list_editable = ['price', 'available']

    search_fields = ['name','description']
    list_filter = ['category', 'available', 'updated', 'created']
    inlines = [ProductImageInline,]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
