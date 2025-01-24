-- models/staging/stg_accounts.sql

SELECT *
FROM {{ source('dbt_mysql_source', 'accounts') }}
