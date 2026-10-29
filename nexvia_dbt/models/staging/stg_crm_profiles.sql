WITH source AS (
    SELECT *
    FROM {{ source('raw', 'crm_profiles') }}
),

renamed_and_casted AS (
    SELECT
        CAST(user_id AS INT64) AS user_id,
        CAST(customer_persona AS STRING) AS customer_persona,
        CAST(account_manager AS STRING) AS account_manager,
        CAST(loyalty_score AS INT64) AS loyalty_score
    FROM source
)

SELECT * FROM renamed_and_casted