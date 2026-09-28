from pathlib import Path
import logging
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT_PATH = str(PROJECT_ROOT)
if PROJECT_ROOT_PATH in sys.path:
    sys.path.remove(PROJECT_ROOT_PATH)
sys.path.insert(0, PROJECT_ROOT_PATH)

from pipeline.extract import extract_data

from pipeline.transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_order_items
)

from pipeline.load import (
    load_customers,
    load_products,
    load_orders,
    load_order_items
)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(
    __file__
).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True
)


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            LOG_DIR / "pipeline.log"
        ),

        logging.StreamHandler()
    ]
)


logger = logging.getLogger(
    "sales_pipeline"
)


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------

def run_pipeline():

    logger.info(
        "======================================"
    )

    logger.info(
        "PIPELINE STARTED"
    )

    logger.info(
        "======================================"
    )

    try:

        # -------------------------------------------------
        # 1. Determine next order ID
        # -------------------------------------------------

        from pipeline.load import (
            get_max_order_id
        )

        max_order_id = (
            get_max_order_id()
        )

        starting_order_id = (
            max_order_id + 1
        )

        logger.info(
            f"Starting order ID: "
            f"{starting_order_id}"
        )

        # -------------------------------------------------
        # 2. EXTRACT
        # -------------------------------------------------

        logger.info(
            "Starting extraction..."
        )

        (
            customers,
            products,
            orders,
            order_items
        ) = extract_data(

            number_of_orders=100,

            starting_order_id=(
                starting_order_id
            )
        )

        logger.info(
            "Extraction completed."
        )

        # -------------------------------------------------
        # 3. TRANSFORM
        # -------------------------------------------------

        logger.info(
            "Starting transformation..."
        )

        customers = (
            transform_customers(
                customers
            )
        )

        products = (
            transform_products(
                products
            )
        )

        orders = (
            transform_orders(
                orders
            )
        )

        order_items = (
            transform_order_items(
                order_items
            )
        )

        logger.info(
            "Transformation completed."
        )

        # -------------------------------------------------
        # 4. LOAD
        # -------------------------------------------------

        logger.info(
            "Starting database load..."
        )

        customers_loaded = (
            load_customers(
                customers
            )
        )

        products_loaded = (
            load_products(
                products
            )
        )

        orders_loaded = (
            load_orders(
                orders
            )
        )

        order_items_loaded = (
            load_order_items(
                order_items
            )
        )

        # -------------------------------------------------
        # 5. Log results
        # -------------------------------------------------

        logger.info(
            f"Customers loaded: "
            f"{customers_loaded}"
        )

        logger.info(
            f"Products loaded: "
            f"{products_loaded}"
        )

        logger.info(
            f"Orders loaded: "
            f"{orders_loaded}"
        )

        logger.info(
            f"Order items loaded: "
            f"{order_items_loaded}"
        )

        logger.info(
            "======================================"
        )

        logger.info(
            "PIPELINE COMPLETED SUCCESSFULLY"
        )

        logger.info(
            "======================================"
        )

    except Exception as error:

        logger.exception(
            "PIPELINE FAILED"
        )

        raise error


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":

    run_pipeline()