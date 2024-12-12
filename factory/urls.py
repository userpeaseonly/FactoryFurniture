from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products_page, name='products'),
    path('products/create/', views.create_product, name='create_product'),
    path('dealers/', views.dealers_page, name='dealers'),
    path('dealers/create/', views.create_dealer, name='create_dealer'),
    path('orders/', views.orders, name='orders'),
    path('orders/create/', views.create_order, name='create_order'),
]
