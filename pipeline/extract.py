from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd
from faker import Faker


fake = Faker()


# ---------------------------------------------------------
# Project directories
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Generate customers
# ---------------------------------------------------------

def generate_customers(
    number_of_customers=100
):

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

    for customer_id in range(
        1,
        number_of_customers + 1
    ):

        signup_date = (
            datetime.now()
            - timedelta(
                days=random.randint(
                    1,
                    730
                )
            )
        ).date()

        customers.append({

            "customer_id":
                customer_id,

            "customer_name":
                fake.name(),

            "city":
                fake.city(),

            "state":
                random.choice(states),

            "signup_date":
                signup_date
        })

    return pd.DataFrame(customers)


# ---------------------------------------------------------
# Generate products
# ---------------------------------------------------------

def generate_products():

    products = [

        (
            1,
            "Laptop",
            "Electronics",
            65000
        ),

        (
            2,
            "Smartphone",
            "Electronics",
            30000
        ),

        (
            3,
            "Headphones",
            "Electronics",
            2500
        ),

        (
            4,
            "Office Chair",
            "Furniture",
            8000
        ),

        (
            5,
            "Desk",
            "Furniture",
            12000
        ),

        (
            6,
            "Keyboard",
            "Accessories",
            1500
        ),

        (
            7,
            "Mouse",
            "Accessories",
            900
        ),

        (
            8,
            "Monitor",
            "Electronics",
            18000
        ),

        (
            9,
            "Backpack",
            "Accessories",
            2500
        ),

        (
            10,
            "Webcam",
            "Electronics",
            4500
        )
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


# ---------------------------------------------------------
# Generate orders
# ---------------------------------------------------------

def generate_orders(
    number_of_orders,
    customers,
    products,
    starting_order_id
):

    orders = []

    order_items = []

    order_item_id = (
        starting_order_id * 10
    )

    for i in range(
        number_of_orders
    ):

        order_id = (
            starting_order_id + i
        )

        customer_id = random.choice(
            customers[
                "customer_id"
            ].tolist()
        )

        order_date = (
            datetime.now()
            - timedelta(
                days=random.randint(
                    0,
                    30
                )
            )
        ).date()

        status = random.choice(
            [
                "Completed",
                "Completed",
                "Completed",
                "Pending",
                "Cancelled"
            ]
        )

        orders.append({

            "order_id":
                order_id,

            "customer_id":
                customer_id,

            "order_date":
                order_date,

            "status":
                status,

            "updated_at":
                datetime.now()
        })

        # Each order can contain
        # 1 to 3 products

        number_of_products = (
            random.randint(1, 3)
        )

        selected_products = (
            products.sample(
                number_of_products
            )
        )

        for _, product in (
            selected_products.iterrows()
        ):

            quantity = random.randint(
                1,
                5
            )

            order_items.append({

                "order_item_id":
                    order_item_id,

                "order_id":
                    order_id,

                "product_id":
                    product[
                        "product_id"
                    ],

                "quantity":
                    quantity,

                "unit_price":
                    product[
                        "price"
                    ]
            })

            order_item_id += 1

    return (
        pd.DataFrame(orders),
        pd.DataFrame(order_items)
    )


# ---------------------------------------------------------
# Main extraction function
# ---------------------------------------------------------

def extract_data(
    number_of_orders=100,
    starting_order_id=1
):

    print(
        "Starting data extraction..."
    )

    customers = generate_customers(
        100
    )

    products = generate_products()

    orders, order_items = (
        generate_orders(
            number_of_orders,
            customers,
            products,
            starting_order_id
        )
    )

    # Save raw data

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

    print(
        "Data extraction completed."
    )

    print(
        f"Customers: {len(customers)}"
    )

    print(
        f"Products: {len(products)}"
    )

    print(
        f"Orders: {len(orders)}"
    )

    print(
        f"Order Items: {len(order_items)}"
    )

    return (
        customers,
        products,
        orders,
        order_items
    )


if __name__ == "__main__":

    extract_data()