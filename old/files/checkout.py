'''----------------------------------- Model--------------------------------------------'''
from django.db import models
from .cart import Cart
from .cartitem import CartItem
from .product import Product

class CheckOut(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending'
        CONFIRMED = 'confirmed'
        CANCELLED = 'cancelled'
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'checkoutcarts')
    status = models.CharField(max_length=100,default='Pending', choices = StatusChoices.choices)
    checkout_date = models.DateTimeField(auto_now_add=True)
    cart_item = models.ManyToManyField(CartItem)
    is_active = models.BooleanField(default=True)

    def apppr(self,user):
        return user.request.filter(user=user).first()
    @property
    def total_amount(self):
        return self.cart_item.sub_total.sum()
    def __str__(self):
        return f"Checkout for {self.apppr} of {self.Product.name}"

'''----------------------------------- serializers--------------------------------------------'''
from rest_framework import serializers

class CheckOutSerializer(serializers.ModelSerializer):


    total_amount = serializers.CharField(max_length = 60 ,read_only = True)
    Product = serializers.CharField(source='Product.name', read_only=True)
    name = serializers.CharField(source = "cart.user.username", read_only = True)
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(),write_only=True)
    cart_item = serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all(),write_only=True,many=True)
    is_active = serializers.BooleanField(write_only=True)

    def validate_cart_item(self,value):
        if value.cart.user != self.context['request'].user:
            raise serializers.ValidationError("CartItem does not belong to the user")
        return value

    class Meta:
        model = CheckOut
        fields = ['name','Product','status','total_amount','checkout_date','cart','cart_item','is_active' ]

'''-----------------------------------Views--------------------------------------------'''
from rest_framework import viewsets

class CheckOutViews(viewsets.ModelViewSet):
    queryset = CheckOut.objects.all()
    serializer_class = CheckOutSerializer

    def perform_create(self, serializer):   
        for item in checkout.cart_item.all():
            item.is_active = False
            item.save()
        cart, created = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        serializer.save(cart=cart)
