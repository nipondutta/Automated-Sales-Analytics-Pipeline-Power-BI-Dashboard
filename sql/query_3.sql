-- Create category performance view

CREATE OR REPLACE VIEW category_sales AS

SELECT

    category,

    SUM(sales_amount)
        AS total_sales,

    SUM(quantity)
        AS total_quantity,

    COUNT(
        DISTINCT order_id
    ) AS total_orders

FROM sales_summary

WHERE status = 'Completed'

GROUP BY category

ORDER BY total_sales DESC;