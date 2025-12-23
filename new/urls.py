from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from old.files.product import ProductViews
from old.files.cart import CartViews
from old.files.cartitem import CartItemviews
from old.files.checkout import CheckOutViews
from old.files.order import OrderViews
from old.files.users import UserViewSet

router = DefaultRouter()
router.register('product', ProductViews, basename = 'product')
router.register('users', UserViewSet)
router.register('checkout', CheckOutViews, basename='checkout')
router.register('cart', CartViews,basename= 'cart')
router.register('cartitem', CartItemviews,basename= 'cartitem')
router.register('order', OrderViews,basename= 'order')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]




