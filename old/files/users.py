from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAdminUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', "password",'email', 'is_staff']

    def create(self, Validated):
        user = User.objects.create_user(
            user_name = Validated['username'],
            email = Validated['email'],
            password = Validated['password']
        )
        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
