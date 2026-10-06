from django.db import models
from django.utils import timezone
from django.conf import settings

# from task.models import Address

# User's Profile
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        primary_key=True,
    )
    phone = models.CharField(max_length=20, blank=True,null=True)
    address = models.TextField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


# class Customer(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20)
#     created_at = models.DateTimeField(default=timezone.now)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)  # Add this field
    created_at = models.DateTimeField(default=timezone.now)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses',
    )


class Category(models.Model):
    name = models.CharField(max_length=100)
    hex_color = models.CharField(max_length=7, default='#000000')


class Collection(models.Model):
    title = models.CharField(max_length=200)


class Promotion(models.Model):
    note = models.CharField(max_length=200)
    discount = models.DecimalField(max_digits=5, decimal_places=2)


class Product(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='products',
    )
    promotions = models.ManyToManyField(
        Promotion,
        blank=True,
        related_name='products',
    )


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    ]

    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
    )


class OrderItem(models.Model):
    qty = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
    )