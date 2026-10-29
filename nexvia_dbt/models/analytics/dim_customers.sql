WITH users AS (
    SELECT * FROM {{ ref('stg_thelook__users') }}
),

crm AS (
    SELECT * FROM {{ ref('stg_crm_profiles') }}
),

customer_360 AS (
    SELECT
        u.user_id,
        u.age,
        u.gender,
        u.country,
        u.account_created_at,
        c.customer_persona,
        c.account_manager,
        c.loyalty_score
    FROM users u
    -- Using an INNER JOIN bcz we want to ensure we only keep the 100k users that we generated CRM data.
    INNER JOIN crm c 
        ON u.user_id = c.user_id
)

SELECT * FROM customer_360