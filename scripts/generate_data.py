import pandas as pd
import pandas_gbq  # Imported directly to avoid pandas version errors
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# 1. Bulletproof pathing for the Google Cloud JSON key
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(BASE_DIR, 'gcp-key.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

PROJECT_ID = 'nexvia-analytics-project' 

# Enforce Reproducibility with Seeds
random.seed(42)
Faker.seed(42)
fake = Faker()

print("Generating Ad Spend Data...")
channels = ['Google Ads', 'Facebook Ads', 'Email', 'Organic Search', 'Twitter']
ad_spend_data = []

# Hardcode the date window so dashboards never shift
fixed_end_date = datetime(2026, 10, 31)
start_date = fixed_end_date - timedelta(days=30)

for i in range(30):
    current_date = start_date + timedelta(days=i)
    for channel in channels:
        impressions = random.randint(1000, 50000)
        ctr = random.uniform(0.01, 0.05)
        clicks = int(impressions * ctr)
        
        # Logical Marketing Spend: Organic Search is unpaid traffic
        if channel == 'Organic Search':
            spend = 0.0
        else:
            spend = round(random.uniform(100.0, 1000.0), 2)
            
        ad_spend_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'campaign_channel': channel,
            'spend': spend,
            'impressions': impressions,
            'clicks': clicks
        })

df_ad_spend = pd.DataFrame(ad_spend_data)
df_ad_spend['date'] = pd.to_datetime(df_ad_spend['date'])

print("Fetching actual user IDs from BigQuery...")
query = """
    SELECT id 
    FROM `bigquery-public-data.thelook_ecommerce.users` 
    LIMIT 100000
"""
# FIX: Use pandas_gbq directly to read the data
df_users = pandas_gbq.read_gbq(query, project_id=PROJECT_ID)
real_user_ids = df_users['id'].tolist()

print(f"Fetched {len(real_user_ids)} real user IDs. Generating CRM profiles...")

crm_data = []
for user_id in real_user_ids:  
    crm_data.append({
        'user_id': user_id,
        'customer_persona': random.choice(['Budget Shopper', 'Impulse Buyer', 'Brand Loyalist', 'Window Shopper']),
        'account_manager': fake.name(),
        'loyalty_score': random.randint(1, 100)
    })

df_crm = pd.DataFrame(crm_data)

print("Uploading to BigQuery (this may take a minute)...")

# FIX: Use pandas_gbq directly to upload the Ad Spend data
pandas_gbq.to_gbq(
    df_ad_spend,
    destination_table='raw_data.ad_spend',
    project_id=PROJECT_ID,
    if_exists='replace'
)
print("Ad Spend uploaded successfully!")

# FIX: Use pandas_gbq directly to upload the CRM data
pandas_gbq.to_gbq(
    df_crm,
    destination_table='raw_data.crm_profiles',
    project_id=PROJECT_ID,
    if_exists='replace'
)
print("CRM Data uploaded successfully! Data Engineering complete.")