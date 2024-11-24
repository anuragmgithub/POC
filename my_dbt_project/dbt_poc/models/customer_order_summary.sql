-- models/customer_order_summary.sql

WITH order_data AS (
    SELECT
        customer_id,
        COUNT(order_id) AS total_orders,
        SUM(total_amount) AS total_spent,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM
        mypoc.orders  -- Referencing the orders table
    GROUP BY
        customer_id
)

SELECT
    customer_id,
    total_orders,
    total_spent,
    first_order_date,
    last_order_date
FROM
    order_data

