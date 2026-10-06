from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import (
	AddressListViewSet,
	CollectionListViewSet,
	CustomerListViewSet,
	OrderItemListViewSet,
	OrderListViewSet,
	ProductListViewSet,
	PromotionListViewSet,
    ProfileAPIView,
)

router = DefaultRouter()
router.register('customers', CustomerListViewSet)
router.register('addresses', AddressListViewSet)
router.register('collections', CollectionListViewSet)
router.register('promotions', PromotionListViewSet)
router.register('products', ProductListViewSet)
router.register('orders', OrderListViewSet)
router.register('order-items', OrderItemListViewSet)
# router.register('users/me/profile', ProfileAPIView.as_view())


customer_router = NestedDefaultRouter(router, 'customers', lookup='customer')
customer_router.register('addresses', AddressListViewSet, basename='customer-addresses')
customer_router.register('orders', OrderListViewSet, basename='customer-orders')

collection_router = NestedDefaultRouter(router, 'collections', lookup='collection')
collection_router.register('products', ProductListViewSet, basename='collection-products')

promotion_router = NestedDefaultRouter(router, 'promotions', lookup='promotion')
promotion_router.register('products', ProductListViewSet, basename='promotion-products')

order_router = NestedDefaultRouter(router, 'orders', lookup='order')
order_router.register('items', OrderItemListViewSet, basename='nested-order-items')

product_router = NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('order-items', OrderItemListViewSet, basename='product-order-items')

# urlpatterns = (
#     path('users/me/profile/', ProfileAPIView.as_view()),
#     router.urls
#     + customer_router.urls
#     + collection_router.urls
#     + promotion_router.urls
#     + order_router.urls
#     + product_router.urls
# )

urlpatterns = [
    path('users/me/profile/', ProfileAPIView.as_view()),
] + router.urls + customer_router.urls + collection_router.urls + promotion_router.urls + order_router.urls + product_router.urls




# urlpatterns = [

#     path('',include(router.urls))
# ]



    


  



