--Create monthly_sales view

CREATE OR REPLACE VIEW monthly_sales AS

SELECT

    DATE_TRUNC(
        'month',
        order_date
    ) AS month,

    SUM(sales_amount)
        AS total_sales,

    SUM(quantity)
        AS total_quantity,

    COUNT(
        DISTINCT order_id
    ) AS total_orders

FROM sales_summary

WHERE status = 'Completed'

GROUP BY
    DATE_TRUNC(
        'month',
        order_date
    )

ORDER BY month;