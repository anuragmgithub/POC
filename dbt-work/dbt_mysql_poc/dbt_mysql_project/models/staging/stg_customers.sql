-- models/staging/stg_customers.sql
SELECT *
FROM {{ source('dbt_mysql_source', 'customers') }}
