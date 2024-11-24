-- models/staging/clean_orders.sql

WITH cleaned_orders AS (
    SELECT
        order_id,
        customer_id,
        CAST(order_amount AS DECIMAL(10, 2)) AS order_amount,
        {{ date_trunc('order_date', 'month') }} AS order_month ,
        {{ date_trunc('order_date', 'year') }} AS order_year  -- Using the macro
    FROM {{ ref('raw_orders') }}
)
SELECT * FROM cleaned_orders
