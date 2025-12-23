'''----------------------------------- Model--------------------------------------------'''

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()

    @property
    def in_stock(self):
        if self.stock > 0:
            return f"out of Stock {False}"
        else:
            return True

    def __str__(self):
        return self.name

'''----------------------------------- serializers--------------------------------------------'''

from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock']

'''-----------------------------------Views--------------------------------------------'''

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination

# class pagesize(LimitOffsetPagination):


#     default_limit = 2
#     max_limit = 4


class ProductViews(ModelViewSet):


    queryset = Product.objects.all()
    serializer_class = ProductSerializer


