WITH customer_totals AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) AS order_count,
        SUM(o.order_amount) AS total_spent
    FROM {{ ref('raw_customers') }} c
    LEFT JOIN {{ ref('clean_orders') }} o
    ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT * FROM customer_totals
