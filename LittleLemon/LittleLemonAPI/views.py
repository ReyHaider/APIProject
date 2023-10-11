from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, UserGroupSerializer
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist


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


class ManagerView(generics.ListCreateAPIView):
    users = User.objects.filter(groups__name='Manager')
    queryset = [{'username': user.username,
                 'email': user.email} for user in users]
    permission_classes = [IsAuthenticated]
    serializer_class = UserGroupSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            users = User.objects.filter(groups__name='Manager')
            queryset = [{'username': user.username,
                         'email': user.email} for user in users]
            return Response({'details': queryset})
        else:
            return Response(f'403 - Unauthorized', status=403)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username=username)
                manager = Group.objects.get(name='Manager')
                manager.user_set.add(user)
                return Response("User added to group manager", status=201)
            else:
                return Response("field : 'username' required", status=404)
        else:
            return Response(f'403 - Unauthorized', status=403)


class DeleteManagerView(generics.RetrieveDestroyAPIView):
    users = User.objects.filter(groups__name='Manager')
    queryset = [{'username': user.username,
                 'password': user.password,
                 'email': user.email} for user in users]
    permission_classes = [IsAuthenticated]
    serializer_class = UserGroupSerializer

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            lookup_url_kwarg = self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )
            pk = self.kwargs[lookup_url_kwarg]
            try:
                user = User.objects.filter(id=pk).get()
            except ObjectDoesNotExist:
                user = None
            if user:
                managers = Group.objects.get(name='Manager')
                managers.user_set.remove(user)
                return Response('200 - Success', status=200)
            else:
                return Response('404 - Not found', status=404)
        else:
            return Response(f'403 - Unauthorized', status=403)


class DeliveryCrewView(generics.ListCreateAPIView):
    users = User.objects.filter(groups__name='Delivery crew')
    queryset = [{'username': user.username,
                 'email': user.email} for user in users]
    permission_classes = [IsAuthenticated]
    serializer_class = UserGroupSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            users = User.objects.filter(groups__name='Delivery crew')
            queryset = [{'username': user.username,
                         'email': user.email} for user in users]
            return Response({'details': queryset})
        else:
            return Response(f'403 - Unauthorized', status=403)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username=username)
                rider = Group.objects.get(name='Delivery crew')
                rider.user_set.add(user)
                return Response("User added to group Delivery crew", status=201)
            else:
                return Response("field : 'username' required", status=404)
        else:
            return Response(f'403 - Unauthorized', status=403)


class DeleteDeliveryCrewView(generics.RetrieveDestroyAPIView):
    users = User.objects.filter(groups__name='Delivery crew')
    queryset = [{'username': user.username,
                 'password': user.password,
                 'email': user.email} for user in users]
    permission_classes = [IsAuthenticated]
    serializer_class = UserGroupSerializer

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            lookup_url_kwarg = self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )
            pk = self.kwargs[lookup_url_kwarg]
            try:
                user = User.objects.filter(id=pk).get()
            except ObjectDoesNotExist:
                user = None
            if user:
                rider = Group.objects.get(name='Delivery crew')
                rider.user_set.remove(user)
                return Response('200 - Success', status=200)
            else:
                return Response('404 - Not found', status=404)
        else:
            return Response(f'403 - Unauthorized', status=403)
