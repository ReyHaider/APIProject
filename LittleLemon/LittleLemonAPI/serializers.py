from rest_framework import serializers
from .models import MenuItem, Category, Cart
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


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('user', 'price', 'unit_price')

    def create(self, validated_data):
        # Get the user from the request
        user = self.context['request'].user

        # Get the menuitem from the validated data
        menuitem = validated_data['menuitem']

        # Retrieve the corresponding MenuItem instance
        menuitem_instance = MenuItem.objects.get(pk=menuitem.pk)

        # Calculate the unit_price as the price of the MenuItem
        unit_price = menuitem_instance.price

        # Calculate the total price as the unit_price * quantity
        quantity = validated_data['quantity']
        price = unit_price * quantity

        cart = Cart.objects.create(
            user=user,
            menuitem=menuitem,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )

        return cart
