'''----------------------------------- Model--------------------------------------------'''
from django.db import models
from .order import order
from .product import Product

class orderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order of {self.order.checkout.cart.user.username}"

'''----------------------------------- serializers--------------------------------------------'''

from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderItem
        fields = '__all__'

'''-----------------------------------Views--------------------------------------------'''
from rest_framework import generics

