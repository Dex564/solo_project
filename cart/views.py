from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import JsonResponse

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Определяем, это AJAX запрос или обычный
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    quantity = int(request.POST.get('quantity', 1))
    update = request.POST.get('update', 'false').lower() == 'true'
    
    cart.add(
        product=product,
        quantity=quantity,
        update_quantity=update
    )
    
    if is_ajax:
        # Для AJAX запросов возвращаем JSON
        return JsonResponse({
            'success': True,
            'cart_total_items': len(cart),
            'cart_total_price': cart.get_total_price(),
            'message': f'{product.name} добавлен в корзину'
        })
    else:
        # Для обычных запросов - редирект в корзину
        return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')