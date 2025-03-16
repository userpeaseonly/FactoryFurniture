from django.contrib import admin

from .models import Product, Dealer, Order, OrderItem, FutureStock

admin.site.register(Product)
admin.site.register(Dealer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(FutureStock)