from django.contrib import admin

from .models import Product, Dealer, Order, OrderItem

admin.site.register(Product)
admin.site.register(Dealer)
admin.site.register(Order)
admin.site.register(OrderItem)