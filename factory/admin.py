from django.contrib import admin

from .models import Product, Dealer, Order

admin.site.register(Product)
admin.site.register(Dealer)
admin.site.register(Order)