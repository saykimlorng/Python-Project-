import json
import random
from datetime import date, datetime, timedelta

# Update "task" to match your app name in INSTALLED_APPS
APP_NAME = "task"

# Helper data pools
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"
]
STREET_NAMES = ["Main St", "Oak Ave", "Maple Rd", "Cedar Ln", "Washington St", "Lake Dr", "Park Ave", "5th Ave"]
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
COLLECTION_PREFIXES = ["Summer", "Winter", "Spring", "Autumn", "Holiday", "Urban", "Vintage", "Modern", "Classic", "Premium"]
COLLECTION_TYPES = ["Deals", "Essentials", "Collection", "Editions", "Selection", "Line", "Series"]
CATEGORY_BASES = ["Tech", "Apparel", "Home Goods", "Sports", "Beauty", "Toys", "Automotive", "Garden", "Jewelry", "Groceries"]

data = []
RECORDS_PER_MODEL = 50

pk_counters = {
    "category": 1,
    "collection": 1,
    "promotion": 1,
    "product": 1,
    "customer": 1,
    "address": 1,
    "order": 1,
    "orderitem": 1,
}

# 1. Categories (50)
category_pks = []
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["category"]
    category_pks.append(pk)
    base_name = random.choice(CATEGORY_BASES)
    data.append({
        "model": f"{APP_NAME}.category",
        "pk": pk,
        "fields": {
            "name": f"{base_name} Category #{i}",
            "hex_color": f"#{random.randint(0, 0xFFFFFF):06X}"
        }
    })
    pk_counters["category"] += 1

# 2. Collections (50)
collection_pks = []
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["collection"]
    collection_pks.append(pk)
    title = f"{random.choice(COLLECTION_PREFIXES)} {random.choice(COLLECTION_TYPES)} #{i}"
    data.append({
        "model": f"{APP_NAME}.collection",
        "pk": pk,
        "fields": {"title": title}
    })
    pk_counters["collection"] += 1

# 3. Promotions (50)
promotion_pks = []
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["promotion"]
    promotion_pks.append(pk)
    discount_val = random.choice([5.00, 10.00, 15.00, 20.00, 25.00, 30.00, 50.00])
    data.append({
        "model": f"{APP_NAME}.promotion",
        "pk": pk,
        "fields": {
            "note": f"Promo Discount Deal #{i}",
            "discount": f"{discount_val:.2f}"
        }
    })
    pk_counters["promotion"] += 1

# 4. Products (50)
product_pks = []
product_prices = {}
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["product"]
    product_pks.append(pk)
    price = round(random.uniform(10.0, 500.0), 2)
    product_prices[pk] = price

    # Assign 0 to 3 random promotions per product
    assigned_promos = random.sample(promotion_pks, k=random.randint(0, 3))

    data.append({
        "model": f"{APP_NAME}.product",
        "pk": pk,
        "fields": {
            "title": f"Product Item #{i}",
            "desc": f"Automated product description details for item inventory #{i}.",
            "price": f"{price:.2f}",
            "inventory": random.randint(10, 300),
            "last_update": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "collection": random.choice(collection_pks),
            "promotions": assigned_promos
        }
    })
    pk_counters["product"] += 1

# 5. Customers (50)
customer_pks = []
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["customer"]
    customer_pks.append(pk)
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    birth = date(1975, 1, 1) + timedelta(days=random.randint(0, 12000))

    data.append({
        "model": f"{APP_NAME}.customer",
        "pk": pk,
        "fields": {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}{pk}@example.com",
            "phone": f"+1555{random.randint(1000000, 9999999)}",
            "birth_date": birth.isoformat(),
            "gender": random.choice(["M", "F"]),
            "status": True
        }
    })
    pk_counters["customer"] += 1

# 6. Addresses (50)
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["address"]
    data.append({
        "model": f"{APP_NAME}.address",
        "pk": pk,
        "fields": {
            "street": f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)}",
            "city": random.choice(CITIES),
            "customer": random.choice(customer_pks)
        }
    })
    pk_counters["address"] += 1

# 7. Orders (50)
order_pks = []
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["order"]
    order_pks.append(pk)
    order_date = datetime.now() - timedelta(days=random.randint(1, 90))
    data.append({
        "model": f"{APP_NAME}.order",
        "pk": pk,
        "fields": {
            "order_date": order_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": random.choice(["P", "C", "F"]),
            "customer": random.choice(customer_pks)
        }
    })
    pk_counters["order"] += 1

# 8. Order Items (50)
for i in range(1, RECORDS_PER_MODEL + 1):
    pk = pk_counters["orderitem"]
    prod_id = random.choice(product_pks)
    data.append({
        "model": f"{APP_NAME}.orderitem",
        "pk": pk,
        "fields": {
            "order": random.choice(order_pks),
            "product": prod_id,
            "qty": random.randint(1, 10),
            "unit_price": f"{product_prices[prod_id]:.2f}"
        }
    })
    pk_counters["orderitem"] += 1

# Output to JSON fixture file
output_file = "fixtures.json"
with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print(f"Successfully generated {len(data)} total records (50 per model) into '{output_file}'!")