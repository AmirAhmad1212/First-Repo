'''----------------------------------- Model--------------------------------------------'''
from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'users')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

'''----------------------------------- serializers--------------------------------------------'''
from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source = "user.username", read_only = True)
    class Meta:
        model = Cart
        fields = ['id','user_name','is_active']


'''-----------------------------------Views--------------------------------------------'''
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class CartViews(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)