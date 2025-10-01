from django.shortcuts import render
from .models import Category, Product
# Create your views here.


def main_page(request):
    return render(request, 'main/base.html')

def products_list(request):
    products = Product.objects.filter(available=True)

    return render(request, 'main/products_list.html',
                {
                    'products': products 
                })

