from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User, Group


class CategoriesView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            return super().post(request, *args, **kwargs)
        else:
            return Response(f'403 - Unauthorized', status=403)


class SingleMenuItemsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            return super().put(request, *args, **kwargs)
        else:
            return Response(f'403 - Unauthorized', status=403)

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            return super().patch(request, *args, **kwargs)
        else:
            return Response(f'403 - Unauthorized', status=403)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            return super().delete(request, *args, **kwargs)
        else:
            return Response(f'403 - Unauthorized', status=403)
