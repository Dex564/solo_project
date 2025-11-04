from django.conf import settings
from main.models import Product
from .models import Cart as CartModel, CartItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.user = request.user
        
        # Для сессионной корзины
        self.session_cart_key = f"{settings.CART_SESSION_ID}_session"
        session_cart = self.session.get(self.session_cart_key, {})
        self.session_cart = session_cart
        
        # Для БД корзины
        self.db_cart = None
        if self.user.is_authenticated:
            self.db_cart, created = CartModel.objects.get_or_create(user=self.user)

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        
        if self.user.is_authenticated and self.db_cart:
            # Работаем с БД
            cart_item, created = CartItem.objects.get_or_create(
                cart=self.db_cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                if update_quantity:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.save()
        else:
            # Работаем с сессией
            if product_id not in self.session_cart:
                self.session_cart[product_id] = {
                    'quantity': 0,
                    'price': str(product.price),
                    'name': product.name
                }
            
            if update_quantity:
                self.session_cart[product_id]['quantity'] = quantity
            else:
                self.session_cart[product_id]['quantity'] += quantity
            
            self._save_session()

    def remove(self, product):
        product_id = str(product.id)
        
        if self.user.is_authenticated and self.db_cart:
            CartItem.objects.filter(cart=self.db_cart, product=product).delete()
        else:
            if product_id in self.session_cart:
                del self.session_cart[product_id]
                self._save_session()

    def __iter__(self):
        if self.user.is_authenticated and self.db_cart:
            # Данные из БД
            for item in self.db_cart.items.select_related('product').all():
                yield {
                    'product': item.product,
                    'quantity': item.quantity,
                    'price': float(item.product.price),
                    'total_price': item.get_total_price(),
                    'name': item.product.name
                }
        else:
            # Данные из сессии
            product_ids = self.session_cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            product_dict = {str(product.id): product for product in products}
            
            for product_id, item_data in self.session_cart.items():
                product = product_dict.get(product_id)
                if product:
                    yield {
                        'product': product,
                        'quantity': item_data['quantity'],
                        'price': float(item_data['price']),
                        'total_price': float(item_data['price']) * item_data['quantity'],
                        'name': item_data['name']
                    }

    def __len__(self):
        if self.user.is_authenticated and self.db_cart:
            return self.db_cart.get_total_quantity()
        else:
            return sum(item['quantity'] for item in self.session_cart.values())

    def get_total_price(self):
        if self.user.is_authenticated and self.db_cart:
            return self.db_cart.get_total_price()
        else:
            return sum(float(item['price']) * item['quantity'] for item in self.session_cart.values())

    def clear(self):
        if self.user.is_authenticated and self.db_cart:
            self.db_cart.items.all().delete()
        else:
            self.session_cart = {}
            self._save_session()

    def _save_session(self):
        self.session[self.session_cart_key] = self.session_cart
        self.session.modified = True

    def merge_carts(self, user):
        """Объединяет сессионную корзину с БД корзиной при логине"""
        if not self.session_cart:
            return
            
        # Получаем или создаем корзину пользователя
        db_cart, created = CartModel.objects.get_or_create(user=user)
        
        # Объединяем товары
        for product_id, item_data in self.session_cart.items():
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=db_cart,
                product=product
            )
            if created:
                cart_item.quantity = item_data['quantity']
            else:
                cart_item.quantity += item_data['quantity']
            cart_item.save()
        
        # Очищаем сессионную корзину
        self.session_cart = {}
        self._save_session()
        
        # Обновляем ссылку на БД корзину
        self.db_cart = db_cart