-- models/marts/mart_combined.sql
WITH customer_data AS (
    SELECT customer_id, first_name, last_name, email
    FROM {{ ref('stg_customers') }}
),
account_data AS (
    SELECT account_id, customer_id, balance, account_type
    FROM {{ ref('stg_accounts') }}
),
transaction_data AS (
    SELECT transaction_id, account_id, amount, transaction_type, transaction_date
    FROM {{ ref('stg_transactions') }}
)
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    a.account_id,
    a.balance,
    t.transaction_id,
    t.amount
FROM customer_data c
JOIN account_data a ON c.customer_id = a.customer_id
JOIN transaction_data t ON a.account_id = t.account_id
