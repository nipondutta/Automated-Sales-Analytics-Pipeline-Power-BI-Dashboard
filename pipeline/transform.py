import pandas as pd


# ---------------------------------------------------------
# Transform customers
# ---------------------------------------------------------

def transform_customers(df):

    df = df.copy()

    # Remove duplicate customers

    df = df.drop_duplicates(
        subset=["customer_id"]
    )

    # Convert signup date

    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )

    # Remove records with missing IDs

    df = df[
        df["customer_id"].notna()
    ]

    # Remove records with missing names

    df = df[
        df["customer_name"].notna()
    ]

    return df


# ---------------------------------------------------------
# Transform products
# ---------------------------------------------------------

def transform_products(df):

    df = df.copy()

    # Remove duplicate products

    df = df.drop_duplicates(
        subset=["product_id"]
    )

    # Convert price to numeric

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Remove invalid prices

    df = df[
        df["price"] >= 0
    ]

    return df


# ---------------------------------------------------------
# Transform orders
# ---------------------------------------------------------

def transform_orders(df):

    df = df.copy()

    # Remove duplicate orders

    df = df.drop_duplicates(
        subset=["order_id"]
    )

    # Convert dates

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    df["updated_at"] = pd.to_datetime(
        df["updated_at"],
        errors="coerce"
    )

    # Remove missing IDs

    df = df[
        df["order_id"].notna()
    ]

    df = df[
        df["customer_id"].notna()
    ]

    # Keep only valid statuses

    valid_statuses = [
        "Completed",
        "Pending",
        "Cancelled"
    ]

    df = df[
        df["status"].isin(
            valid_statuses
        )
    ]

    return df


# ---------------------------------------------------------
# Transform order items
# ---------------------------------------------------------

def transform_order_items(df):

    df = df.copy()

    # Convert numeric columns

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    # Remove duplicates

    df = df.drop_duplicates(
        subset=["order_item_id"]
    )

    # Valid quantities

    df = df[
        df["quantity"] > 0
    ]

    # Valid prices

    df = df[
        df["unit_price"] >= 0
    ]

    return df