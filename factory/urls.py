from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('products/', views.products_page, name='products'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

    path('dealers/', views.dealers_page, name='dealers'),
    path('dealers/create/', views.create_dealer, name='create_dealer'),
    path('dealers/edit/<int:pk>/', views.edit_dealer, name='edit_dealer'),
    path('dealers/delete/<int:pk>/', views.delete_dealer, name='delete_dealer'),

    path('orders/', views.orders, name='orders'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),

    path('stocks/manage/', views.manage_stock, name='manage_stock'),

    path('product-stock/', views.product_stock_view, name='product_stock'),

    path('products/manage/<int:pk>/', views.manage_product_stock, name='manage_product_stock'),

    path('products/future-finished/<int:pk>', views.future_stock_finished, name='future_stock_finished'),
]
