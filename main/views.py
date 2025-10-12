from django.shortcuts import render, get_object_or_404
from .models import Category, Product
# Create your views here.


def main_page(request):
    return render(request, 'main/base.html')

def products_list(request):
    products = Product.objects.filter()

    return render(request, 'main/products_list.html',
                {
                    'products': products 
                })

def prouduct_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    
    return render(request, 'main/product_details.html',
                {
                    'product': product,
                })
