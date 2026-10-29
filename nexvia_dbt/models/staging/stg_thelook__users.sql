WITH source AS (
    SELECT *
    FROM {{ source('thelook', 'users') }}
),

renamed_and_casted AS (
    SELECT
        CAST(id AS INT64) AS user_id,
        CAST(age AS INT64) AS age,
        CAST(gender AS STRING) AS gender,
        CAST(country AS STRING) AS country,
        CAST(created_at AS TIMESTAMP) AS account_created_at
    FROM source
)

SELECT * FROM renamed_and_casted