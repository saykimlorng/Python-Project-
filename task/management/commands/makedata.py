from django.core.management.base import BaseCommand
from faker import Faker
from task.models import (
    Category,
    Collection,
    Promotion,
    Product,
    Customer,
    Address,
    Order,
    OrderItem,
)
import random
from decimal import Decimal
from django.db import transaction


class Command(BaseCommand):
    help = "Generate fake data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        fake = Faker()

        number_of_generate = 50

        # Category
        for _ in range(number_of_generate):
            Category.objects.create(
                name=fake.word(),
                hex_color="#{:06x}".format(random.randint(0, 0xFFFFFF))
            )

        collections = []
        for _ in range(number_of_generate):
            collection = Collection.objects.create(
                title=fake.word().title()
            )
            collections.append(collection)

        promotions = []
        for _ in range(number_of_generate):
            promotion = Promotion.objects.create(
                note=fake.sentence(nb_words=3),
                discount=Decimal(random.randint(5, 50))
            )
            promotions.append(promotion)


        products = []
        for _ in range(number_of_generate):
            product = Product.objects.create(
                title=fake.word().title(),
                desc=fake.text(max_nb_chars=100),
                price=Decimal(random.randint(10, 300)),
                inventory=random.randint(1, 100),
                collection=random.choice(collections),
            )

            product.promotions.set(
                random.sample(
                    promotions,
                    random.randint(0, len(promotions))
                )
            )
            products.append(product)


        customers = []
        for _ in range(number_of_generate):
            customer = Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                birth_date=fake.date_of_birth(),
            )
            customers.append(customer)


        for customer in customers:
            Address.objects.create(
                street=fake.street_address(),
                city=fake.city(),
                customer=customer
            )


        orders = []
        for _ in range(number_of_generate):
            order = Order.objects.create(
                customer=random.choice(customers),
                status=random.choice(["P", "C", "X"])
            )
            orders.append(order)


        for order in orders:
            product = random.choice(products)
            OrderItem.objects.create(
                order=order,
                product=product,
                qty=random.randint(1, 5),
                unit_price=product.price
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {number_of_generate} records for each main table."
            )
        ) 
