import pandas as pd
from sqlalchemy import text

from config.config import engine


# ---------------------------------------------------------
# Get current maximum order ID
# ---------------------------------------------------------

def get_max_order_id():

    query = """
        SELECT COALESCE(
            MAX(order_id),
            0
        )
        FROM orders;
    """

    with engine.connect() as connection:

        result = connection.execute(
            text(query)
        )

        max_order_id = result.scalar()

    return int(max_order_id)


# ---------------------------------------------------------
# Load customers
# ---------------------------------------------------------

def load_customers(df):

    existing = pd.read_sql(
        "SELECT customer_id FROM customers",
        engine
    )

    new_records = df[
        ~df["customer_id"].isin(
            existing["customer_id"]
        )
    ]

    if new_records.empty:

        print(
            "No new customers to load."
        )

        return 0

    new_records.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )

    return len(new_records)


# ---------------------------------------------------------
# Load products
# ---------------------------------------------------------

def load_products(df):

    existing = pd.read_sql(
        "SELECT product_id FROM products",
        engine
    )

    new_records = df[
        ~df["product_id"].isin(
            existing["product_id"]
        )
    ]

    if new_records.empty:

        print(
            "No new products to load."
        )

        return 0

    new_records.to_sql(
        "products",
        engine,
        if_exists="append",
        index=False
    )

    return len(new_records)


# ---------------------------------------------------------
# Load orders
# ---------------------------------------------------------

def load_orders(df):

    existing = pd.read_sql(
        "SELECT order_id FROM orders",
        engine
    )

    new_records = df[
        ~df["order_id"].isin(
            existing["order_id"]
        )
    ]

    if new_records.empty:

        print(
            "No new orders to load."
        )

        return 0

    new_records.to_sql(
        "orders",
        engine,
        if_exists="append",
        index=False
    )

    return len(new_records)


# ---------------------------------------------------------
# Load order items
# ---------------------------------------------------------

def load_order_items(df):

    existing = pd.read_sql(
        """
        SELECT order_item_id
        FROM order_items
        """,
        engine
    )

    new_records = df[
        ~df["order_item_id"].isin(
            existing["order_item_id"]
        )
    ]

    if new_records.empty:

        print(
            "No new order items to load."
        )

        return 0

    new_records.to_sql(
        "order_items",
        engine,
        if_exists="append",
        index=False
    )

    return len(new_records)