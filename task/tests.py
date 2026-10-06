from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Address, Collection, Customer, Order, OrderItem, Product, Promotion


class ProfileSyncTests(TestCase):
    def test_profile_update_updates_user_contact_information(self):
        user = get_user_model().objects.create_user(
            username='profile-user',
            email='profile@example.com',
            password='test-password',
        )
        profile = user.profile
        profile.phone = '+123456789'
        profile.address = 'Updated address'
        profile.save()

        user.refresh_from_db()
        self.assertEqual(user.phone, '+123456789')
        self.assertEqual(user.address, 'Updated address')

    def test_profile_bio_is_stored_on_profile(self):
        user = get_user_model().objects.create_user(
            username='profile-bio-user',
            email='bio@example.com',
            password='test-password',
        )

        profile = user.profile
        profile.bio = 'Loves coding and hiking.'
        profile.save()

        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'Loves coding and hiking.')


class ModelRelationshipTests(TestCase):
    def test_product_can_belong_to_a_collection_and_have_promotions(self):
        collection = Collection.objects.create(title="New Arrivals")
        promotion = Promotion.objects.create(note="Holiday Sale", discount=Decimal("10.00"))
        product = Product.objects.create(
            title="Smartphone",
            desc="A modern phone",
            price=Decimal("599.99"),
            inventory=25,
            collection=collection,
        )
        product.promotions.add(promotion)

        self.assertEqual(product.collection, collection)
        self.assertIn(product, collection.products.all())
        self.assertIn(promotion, product.promotions.all())


class ProductApiTests(TestCase):
    def setUp(self):
        self.collection = Collection.objects.create(title="New Arrivals")

    def create_product(self, title="Laptop"):
        return Product.objects.create(
            title=title,
            desc="Product description",
            price=Decimal("1499.99"),
            inventory=10,
            collection=self.collection,
        )

    def test_product_list_filters_by_title(self):
        self.create_product("Laptop")
        self.create_product("Mouse")

        response = self.client.get('/api/v1/products/?title=Laptop')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['title'], 'Laptop')

    def test_product_detail_update_and_delete(self):
        product = self.create_product()

        detail_response = self.client.get(f'/api/v1/products/{product.id}/')
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()['title'], 'Laptop')

        updated = self.client.patch(
            f'/api/v1/products/{product.id}/',
            {'price': '1799.99'},
            content_type='application/json',
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(Decimal(updated.json()['price']), Decimal('1799.99'))

        deleted = self.client.delete(f'/api/v1/products/{product.id}/')
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Product.objects.filter(id=product.id).exists())


class ApiRouteTests(TestCase):
    def test_all_registered_list_routes_are_available(self):
        collection = Collection.objects.create(title='Best Sellers')
        promotion = Promotion.objects.create(note='Weekend Deal', discount=Decimal('15.00'))
        customer = Customer.objects.create(
            first_name='Bob', last_name='Smith', email='bob@example.com', phone='9988776655'
        )
        product = Product.objects.create(
            title='Headphones', desc='Wireless audio', price=Decimal('199.99'), inventory=8,
            collection=collection,
        )
        product.promotions.add(promotion)
        order = Order.objects.create(customer=customer, status='P')
        address = Address.objects.create(street='123 Main St', city='Dubai', customer=customer)
        item = OrderItem.objects.create(order=order, product=product, qty=2, unit_price=Decimal('199.99'))

        for endpoint in (
            '/api/v1/customers/', '/api/v1/addresses/', '/api/v1/collections/',
            '/api/v1/promotions/', '/api/v1/products/', '/api/v1/orders/', '/api/v1/order-items/',
        ):
            self.assertEqual(self.client.get(endpoint).status_code, 200, endpoint)

        for endpoint in (
            f'/api/v1/customers/{customer.id}/', f'/api/v1/addresses/{address.id}/',
            f'/api/v1/collections/{collection.id}/', f'/api/v1/promotions/{promotion.id}/',
            f'/api/v1/products/{product.id}/', f'/api/v1/orders/{order.id}/',
            f'/api/v1/order-items/{item.id}/',
        ):
            self.assertEqual(self.client.get(endpoint).status_code, 200, endpoint)


class DashboardRouteTests(TestCase):
    def test_dashboard_and_sidebar_routes_render(self):
        for endpoint in ('/', '/tasks/', '/users/'):
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200, endpoint)
