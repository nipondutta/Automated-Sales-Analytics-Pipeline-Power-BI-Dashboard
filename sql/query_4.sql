-- Create customer performance view

CREATE OR REPLACE VIEW customer_sales AS

SELECT

    customer_id,

    customer_name,

    city,

    state,

    COUNT(
        DISTINCT order_id
    ) AS total_orders,

    SUM(sales_amount)
        AS total_sales,

    SUM(quantity)
        AS total_quantity

FROM sales_summary

WHERE status = 'Completed'

GROUP BY

    customer_id,

    customer_name,

    city,

    state;