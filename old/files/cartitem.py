'''----------------------------------- Model--------------------------------------------'''

from django.db import models
from .product import *
from .cart import *
from rest_framework.permissions import IsAuthenticated
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'products')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)
    @property
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        if self.is_active == True:
            return f"{self.quantity} of {self.product.name} in cart of {self.cart.user.username}"
        else:
            return f"{self.product.name} Checked out"


'''----------------------------------- serializers--------------------------------------------'''

from rest_framework import serializers

class CartItemSerializer(serializers.ModelSerializer):


    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all(),write_only = True)
    product_name = serializers.CharField(source = "product.name", read_only = True)
    cart_owner = serializers.CharField(source="cart.user.username", read_only=True)
    sub_total = serializers.ReadOnlyField()
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart']

'''-----------------------------------Views--------------------------------------------'''

from rest_framework import viewsets

class CartItemviews(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):


        cart, created = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        return CartItem.objects.filter(cart=cart, is_active=True)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        serializer.save(cart=cart)
        

    # def get_queryset(self):
    #     user = self.request.user
    #     cart = Cart.objects.get(user=user, is_active=True)
    #     return CartItem.objects.filter(cart=cart)
