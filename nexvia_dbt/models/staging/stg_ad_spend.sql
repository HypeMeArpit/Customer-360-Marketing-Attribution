WITH source AS (
    SELECT *
    FROM {{ source('raw', 'ad_spend') }}
),

renamed_and_casted AS (
    SELECT
        CAST(date AS DATE) AS spend_date,
        CAST(campaign_channel AS STRING) AS campaign_channel,
        CAST(spend AS FLOAT64) AS spend_amount,
        CAST(impressions AS INT64) AS impressions,
        CAST(clicks AS INT64) AS clicks
    FROM source
)

SELECT * FROM renamed_and_casted