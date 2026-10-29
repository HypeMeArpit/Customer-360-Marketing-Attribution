WITH ad_spend AS (
    SELECT * FROM {{ ref('stg_ad_spend') }}
),

marketing_metrics AS (
    SELECT
        spend_date,
        campaign_channel,
        spend_amount,
        impressions,
        clicks,
        -- Calculating Click-Through Rate (CTR) natively in the warehouse.
        CASE 
            WHEN impressions > 0 THEN SAFE_DIVIDE(clicks, impressions) 
            ELSE 0 
        END AS ctr
    FROM ad_spend
)

SELECT * FROM marketing_metrics