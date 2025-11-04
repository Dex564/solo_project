from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from cart.cart import Cart

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Объединяем корзины
            cart = Cart(request)
            cart.merge_carts(user)
            
            login(request, user)
            return redirect('main:main_page')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Объединяем корзины
            cart = Cart(request)
            cart.merge_carts(user)
            
            login(request, user)
            return redirect('main:main_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:main_page')