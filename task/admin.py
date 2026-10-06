from django.contrib import admin
from django.db.models import Count
from . models import Customer, Address, Collection, Product, Order, OrderItem, Promotion, Profile


# admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'address',
        'bio',
        'gender',
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'orders_count')
    search_fields = ('first_name','last_name','phone','email')
    ordering = ('-id',)
    list_per_page =  10

    def orders_count(self, customer):
        return customer.orders_count

    orders_count.short_description = 'Orders Count'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('orders')
        )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'customer_id', 'customer')
    list_filter = ('city',)
    search_fields = ('street', 'city', 'customer__first_name', 'customer__last_name')
    ordering = ('-id',)
    list_per_page =  10


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    search_fields = ('title',)
    ordering = ('-id',)
    list_per_page =  10

    def products_count(self, collection):
        return collection.products_count

    products_count.short_description = 'Products Count'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'inventory', 'collection', 'last_update', 'display_promotions')
    list_filter = ('collection',)
    search_fields = ('title', 'desc')
    list_editable = ['price', 'inventory']
    ordering = ('-last_update',)
    list_per_page =  10

    def display_promotions(self, product):
        promotions = product.promotions.all()
        promotions_list = []
        for promotion in promotions:
            promotions_list.append(promotion.note)
        return ", ".join(promotions_list)

    display_promotions.short_description = 'Promotions'


#one order have many order items, one order item belong to one order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'status', 'customer', 'items_count')
    list_filter = ('status',)
    search_fields = ('id', 'customer__first_name', 'customer__last_name')
    ordering = ('-order_date',)
    list_per_page =  10

    def items_count(self, order):
        return order.items_count

    items_count.short_description = 'Items Count'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('items')
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'qty', 'unit_price')
    search_fields = ('order__id', 'product__title')
    ordering = ('-id',)
    list_per_page =  10

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('note', 'discount', 'products_count', 'display_products')
    search_fields = ('note',)
    ordering = ('-id',)
    list_per_page =  10

    def products_count(self, promotion):
        return promotion.products_count

    products_count.short_description = 'Products Count'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

    def display_products(self, promotion):
        products = promotion.products.all()
        products_with_promotion = []
        for product in products:
            products_with_promotion.append(product.title)
        return ", ".join(products_with_promotion)

    display_products.short_description = 'Products'
