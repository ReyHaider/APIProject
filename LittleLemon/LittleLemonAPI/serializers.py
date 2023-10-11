from rest_framework import serializers
from .models import MenuItem, Category
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    Category_id = serializers.IntegerField(write_only=True)
    Category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price',
                  'featured', 'Category', 'Category_id']


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email',]
        extra_kwargs = {'email': {'read_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserGroupSerializer, self).create(validated_data)
