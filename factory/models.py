from django.db import models

class Dealer(models.Model):
    name = models.CharField(max_length=255)
    phone_number1 = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class DeliveryType(models.TextChoices):
    COLLECTION = 'collection', "Yig'ish"
    DELIVERY = 'delivery', "Yetkazib Berish"
    EXPORTATION = 'exportation', "Olib Ketish"

class Order(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    delivery_type = models.CharField(max_length=20, choices=DeliveryType.choices)
    delivery_date = models.DateTimeField()
    order_cost = models.DecimalField(max_digits=16, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} for {self.dealer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"