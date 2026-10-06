from rest_framework.viewsets import ModelViewSet
from django.db.models import Count 
from django.shortcuts import get_object_or_404, render
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

from .serializers import (
    CustomerSerializer,
    AddressSerializer,
    CollectionSerializer,
    PromotionSerializer,
    ProductSerializer,  
    OrderSerializer,
    OrderItemSerializer,
    ProfileSerializer,
)


def dashboard(request):
    """Render the dashboard available at the site root."""
    return render(request, 'index.html')


# class ProfileViewSet(ModelViewSet):
#     def patch(self, request):
#         profile = request.user.profile
#         serializer = ProfileSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileAPIView(APIView):
    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = PageNumberPagination
    # parser_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        address_id = self.request.query_params.get('address') or self.request.query_params.get('address_id')
        address_city = self.request.query_params.get('city')
        order_id = self.request.query_params.get('order') or self.request.query_params.get('order_id')
        product_id = self.request.query_params.get('product') or self.request.query_params.get('product_id')
        collection_id = self.request.query_params.get('collection') or self.request.query_params.get('collection_id')
        promotion_id = self.request.query_params.get('promotion') or self.request.query_params.get('promotion_id')

        if address_id:
            queryset = queryset.filter(addresses__id=address_id)
        if address_city:
            queryset = queryset.filter(addresses__city__iexact=address_city)
        if order_id:
            queryset = queryset.filter(orders__id=order_id)
        if product_id:
            queryset = queryset.filter(orders__items__product_id=product_id)
        if collection_id:
            queryset = queryset.filter(orders__items__product__collection_id=collection_id)
        if promotion_id:
            queryset = queryset.filter(orders__items__product__promotions__id=promotion_id)

        return queryset.distinct()


class AddressListViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        customer_id = (
            self.kwargs.get('customer_pk') 
            or self.request.query_params.get('customer') 
            or self.request.query_params.get('customer_id')
        )
        address_city = self.request.query_params.get('address_city') or self.request.query_params.get('city')

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if address_city:
            queryset = queryset.filter(city__iexact=address_city)
            
        return queryset

    def perform_create(self, serializer):
        customer_id = self.kwargs.get('customer_pk') or self.request.data.get('customer')
        customer = get_object_or_404(Customer, pk=customer_id)
        serializer.save(customer=customer)


class CollectionListViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')
    )
    serializer_class = CollectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        product_id = self.request.query_params.get('product') or self.request.query_params.get('product_id')
        promotion_id = (
            self.kwargs.get('promotion_pk') 
            or self.request.query_params.get('promotion') 
            or self.request.query_params.get('promotion_id')
        )
        order_id = self.request.query_params.get('order') or self.request.query_params.get('order_id')
        customer_id = self.request.query_params.get('customer') or self.request.query_params.get('customer_id')

        if product_id:
            queryset = queryset.filter(products__id=product_id)
        if promotion_id:
            queryset = queryset.filter(products__promotions__id=promotion_id)
        if order_id:
            queryset = queryset.filter(products__order_items__order_id=order_id)
        if customer_id:
            queryset = queryset.filter(products__order_items__order__customer_id=customer_id)

        return queryset.distinct()


class PromotionListViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        product_id = (
            self.kwargs.get('product_pk') 
            or self.request.query_params.get('product') 
            or self.request.query_params.get('product_id')
        )
        product_name = (
            self.request.query_params.get('products')
            or self.request.query_params.get('product_name')
            or self.request.query_params.get('product_title')
        )
        collection_id = (
            self.kwargs.get('collection_pk') 
            or self.request.query_params.get('collection') 
            or self.request.query_params.get('collection_id')
        )
        order_id = self.request.query_params.get('order') or self.request.query_params.get('order_id')
        customer_id = self.request.query_params.get('customer') or self.request.query_params.get('customer_id')

        if product_id:
            queryset = queryset.filter(products__id=product_id)
        if product_name:
            queryset = queryset.filter(products__title__iexact=product_name)
        if collection_id:
            queryset = queryset.filter(products__collection_id=collection_id)
        if order_id:
            queryset = queryset.filter(products__order_items__order_id=order_id)
        if customer_id:
            queryset = queryset.filter(products__order_items__order__customer_id=customer_id)

        return queryset.distinct()


class ProductListViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        collection_id = (
            self.kwargs.get('collection_pk')
            or self.request.query_params.get('collection') 
            or self.request.query_params.get('collection_id')
            or self.request.query_params.get('collections')
        )
        promotion_id = (
            self.kwargs.get('promotion_pk')
            or self.request.query_params.get('promotion') 
            or self.request.query_params.get('promotion_id')
        )
        order_id = self.request.query_params.get('order') or self.request.query_params.get('order_id')
        customer_id = self.request.query_params.get('customer') or self.request.query_params.get('customer_id')
        title = self.request.query_params.get('title') or self.request.query_params.get('name')

        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        if promotion_id:
            queryset = queryset.filter(promotions__id=promotion_id)
        if order_id:
            queryset = queryset.filter(order_items__order_id=order_id)
        if customer_id:
            queryset = queryset.filter(order_items__order__customer_id=customer_id)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    def perform_create(self, serializer):
        collection_id = self.kwargs.get('collection_pk') or self.request.data.get('collection')
        collection = get_object_or_404(Collection, pk=collection_id)
        product = serializer.save(collection=collection)

        promotion_id = self.kwargs.get('promotion_pk')
        if promotion_id:
            promotion = get_object_or_404(Promotion, pk=promotion_id)
            product.promotions.add(promotion)


class OrderListViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        customer_id = (
            self.kwargs.get('customer_pk') 
            or self.request.query_params.get('customer') 
            or self.request.query_params.get('customer_id')
        )
        product_id = self.request.query_params.get('product') or self.request.query_params.get('product_id')
        collection_id = self.request.query_params.get('collection') or self.request.query_params.get('collection_id')
        promotion_id = self.request.query_params.get('promotion') or self.request.query_params.get('promotion_id')

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if product_id:
            queryset = queryset.filter(items__product_id=product_id)
        if collection_id:
            queryset = queryset.filter(items__product__collection_id=collection_id)
        if promotion_id:
            queryset = queryset.filter(items__product__promotions__id=promotion_id)

        return queryset.distinct()

    def perform_create(self, serializer):
        customer_id = self.kwargs.get('customer_pk') or self.request.data.get('customer')
        customer = get_object_or_404(Customer, pk=customer_id)
        serializer.save(customer=customer)


class OrderItemListViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        order_id = (
            self.kwargs.get('order_pk') 
            or self.request.query_params.get('order') 
            or self.request.query_params.get('order_id')
        )
        product_id = (
            self.kwargs.get('product_pk') 
            or self.request.query_params.get('product') 
            or self.request.query_params.get('product_id')
        )
        customer_id = self.request.query_params.get('customer') or self.request.query_params.get('customer_id')
        collection_id = self.request.query_params.get('collection') or self.request.query_params.get('collection_id')
        promotion_id = self.request.query_params.get('promotion') or self.request.query_params.get('promotion_id')

        if order_id:
            queryset = queryset.filter(order_id=order_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if customer_id:
            queryset = queryset.filter(order__customer_id=customer_id)
        if collection_id:
            queryset = queryset.filter(product__collection_id=collection_id)
        if promotion_id:
            queryset = queryset.filter(product__promotions__id=promotion_id)

        return queryset.distinct()

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_pk') or self.request.data.get('order')
        product_id = self.kwargs.get('product_pk') or self.request.data.get('product')
        order = get_object_or_404(Order, pk=order_id)
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(order=order, product=product)
