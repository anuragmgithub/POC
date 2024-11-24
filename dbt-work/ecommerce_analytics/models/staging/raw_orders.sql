-- models/staging/raw_orders.sql
{{ config(materialized='view') }}

SELECT *
FROM {{ source('ecommerce_source', 'orders') }}

