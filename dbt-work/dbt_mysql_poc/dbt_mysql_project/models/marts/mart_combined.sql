WITH customer_data AS (
    SELECT
        customer_id,
        first_name,
        last_name,
        email
    FROM {{ ref('stg_customers') }}
),
account_data AS (
    SELECT
        account_id,
        customer_id,
        balance,
        account_type
    FROM {{ ref('stg_accounts') }}
),
transaction_data AS (
    SELECT
        transaction_id,
        account_id,
        amount,
        transaction_date
    FROM {{ ref('stg_transactions') }}
)
SELECT 
    {{ dynamic_column_selector(['customer_id', 'first_name', 'last_name', 'email'], 'c') }},
    a.account_id,
    a.balance,
   {{format_date('t.transaction_date', '%Y-%m-%d')}} as transaction_date,
    {{ apply_account_type_logic('a.account_type') }} AS account_type
FROM customer_data c
JOIN account_data a
    ON c.customer_id = a.customer_id
JOIN transaction_data t ON a.account_id = t.account_id

    