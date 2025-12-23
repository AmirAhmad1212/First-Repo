'''----------------------------------- Model--------------------------------------------'''
from django.db import models
from django.contrib.auth.models import User
from .checkout import *


class order(models.Model):
    class statuschoices(models.TextChoices):
        PLACED = 'placed'
        CANCELLED = 'cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout = models.ForeignKey(CheckOut, on_delete=models.CASCADE, related_name='ordercheckout')
    status = models.CharField(max_length=50, choices = statuschoices.choices)
    order_date = models.DateField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum(item.product.price * item.quantity for item in self.checkout.cart_item.all())
    def __str__(self):
        return f"Order of {self.user.username} - {self.status}"
'''----------------------------------- serializers--------------------------------------------'''
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.CharField(read_only=True)
    user_name = serializers.CharField(source='user.username',read_only=True)
    product_name = serializers.CharField(source = 'checkout.cart_item.product.name',read_only=True)

    class Meta:
        model = order
        fields = '__all__'

'''-----------------------------------Views--------------------------------------------'''
from rest_framework import viewsets

class OrderViews(viewsets.ModelViewSet):

    queryset = order.objects.all()
    serializer_class = OrderSerializer


