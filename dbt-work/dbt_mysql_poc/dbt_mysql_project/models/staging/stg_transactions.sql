
SELECT *
FROM {{ source('dbt_mysql_source', 'transactions') }}