--Create sales_summary

CREATE OR REPLACE VIEW sales_summary AS

SELECT

    o.order_id,

    o.order_date,

    o.status,

    o.customer_id,

    c.customer_name,

    c.city,

    c.state,

    p.product_id,

    p.product_name,

    p.category,

    oi.quantity,

    oi.unit_price,

    (
        oi.quantity * oi.unit_price
    ) AS sales_amount

FROM orders o

INNER JOIN customers c
    ON o.customer_id = c.customer_id

INNER JOIN order_items oi
    ON o.order_id = oi.order_id

INNER JOIN products p
    ON oi.product_id = p.product_id;