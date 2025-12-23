from django.contrib import admin
from old.files.cart import Cart
from old.files.cartitem import CartItem
from old.files.order import order
from old.files.orderitems import orderItem
from old.files.product import Product
from old.files.checkout import CheckOut

# Register your models here.


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(CheckOut)
admin.site.register(order)
admin.site.register(orderItem)
