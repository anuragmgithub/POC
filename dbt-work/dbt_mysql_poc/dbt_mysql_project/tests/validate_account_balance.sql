SELECT *
FROM {{ ref('mart_combined') }}
WHERE balance < 7000
