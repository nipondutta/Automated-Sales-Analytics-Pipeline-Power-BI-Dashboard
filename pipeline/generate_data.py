import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(num_customers=100):

    customers = []

    states = [
        "West Bengal",
        "Maharashtra",
        "Karnataka",
        "Tamil Nadu",
        "Delhi",
        "Gujarat",
        "Telangana",
        "Rajasthan"
    ]

    for customer_id in range(1, num_customers + 1):

        customers.append({
            "customer_id": customer_id,
            "customer_name": fake.name(),
            "city": fake.city(),
            "state": random.choice(states),
            "signup_date": fake.date_between(
                start_date="-2y",
                end_date="today"
            )
        })

    return pd.DataFrame(customers)


def generate_products():

    products = [
        (1, "Laptop", "Electronics", 65000),
        (2, "Smartphone", "Electronics", 30000),
        (3, "Headphones", "Electronics", 2500),
        (4, "Office Chair", "Furniture", 8000),
        (5, "Desk", "Furniture", 12000),
        (6, "Keyboard", "Accessories", 1500),
        (7, "Mouse", "Accessories", 900),
        (8, "Monitor", "Electronics", 18000),
        (9, "Backpack", "Accessories", 2500),
        (10, "Webcam", "Electronics", 4500)
    ]

    return pd.DataFrame(
        products,
        columns=[
            "product_id",
            "product_name",
            "category",
            "price"
        ]
    )


def generate_orders(
    num_orders,
    start_order_id,
    customers,
    products
):

    orders = []
    order_items = []

    order_item_id = start_order_id * 10

    for i in range(num_orders):

        order_id = start_order_id + i

        customer_id = random.choice(
            customers["customer_id"].tolist()
        )

        order_date = fake.date_between(
            start_date="-30d",
            end_date="today"
        )

        status = random.choice([
            "Completed",
            "Completed",
            "Completed",
            "Pending",
            "Cancelled"
        ])

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status,
            "updated_at": datetime.now()
        })

        number_of_products = random.randint(1, 3)

        selected_products = products.sample(
            number_of_products
        )

        for _, product in selected_products.iterrows():

            quantity = random.randint(1, 5)

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": product["price"]
            })

            order_item_id += 1

    return (
        pd.DataFrame(orders),
        pd.DataFrame(order_items)
    )


if __name__ == "__main__":

    customers = generate_customers(100)

    products = generate_products()

    orders, order_items = generate_orders(
        num_orders=100,
        start_order_id=1,
        customers=customers,
        products=products
    )

    customers.to_csv(
        RAW_DIR / "customers.csv",
        index=False
    )

    products.to_csv(
        RAW_DIR / "products.csv",
        index=False
    )

    orders.to_csv(
        RAW_DIR / "orders.csv",
        index=False
    )

    order_items.to_csv(
        RAW_DIR / "order_items.csv",
        index=False
    )

    print("Data generated successfully.")