from django.contrib.auth.models import User
import djoser
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

from .models import (
    Customer,
    Address,
    Collection,
    Promotion,
    Product,
    Order,
    OrderItem,
    Profile
)




class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

        fields = [
            'id',
            'street',
            'city',
            'customer'
        ]
        extra_kwargs = {
            'customer': {'required': False},
        }



class CustomerSerializer(serializers.ModelSerializer):

    addresses = AddressSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Customer

        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'created_at',
            'addresses'
        ]



class CollectionSerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Collection

        fields = [
            'id',
            'title',
            'products_count'
        ]



class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion

        fields = [
            'id',
            'note',
            'discount',
            'products'
        ]



class ProductSerializer(serializers.ModelSerializer):

    collection_title = serializers.CharField(
        source='collection.title',
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            'id',
            'title',
            'desc',
            'price',
            'inventory',
            'last_update',
            'collection',
            'collection_title',
            'promotions'
        ]
        extra_kwargs = {
            'collection': {'required': False},
        }



class OrderItemSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source='product.title',
        read_only=True
    )

    class Meta:
        model = OrderItem

        fields = [
            'id',
            'order',
            'product',
            'product_title',
            'qty',
            'unit_price'
        ]
        extra_kwargs = {
            'order': {'required': False},
            'product': {'required': False},
        }



# class OrderSerializer(serializers.ModelSerializer):

#     items = OrderItemSerializer(
#         many=True,
#         read_only=True
#     )

#     customer_name = serializers.StringRelatedField(
#         source='customer',
#         read_only=True
#     )

#     class Meta:
#         model = Order

#         fields = [
#             'id',
#             'order_date',
#             'status',
#             'customer',
#             'customer_name',
#             'items'
#         ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    customer_name = serializers.StringRelatedField(source='customer', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_date',
            'status',
            'customer',
            'customer_name',
            'items'
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['phone', 'address', 'gender']

class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        print("data:", self.initial_data)
        phone = self.initial_data.pop("phone", None)
        user = super().create(validated_data)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                "phone": phone
            }
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', read_only=True)

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  