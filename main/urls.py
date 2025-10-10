from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('products', views.products_list, name='products_list'),
    path('<int:id>/<slug:slug>', views.prouduct_detail, name='product_detail')
]

