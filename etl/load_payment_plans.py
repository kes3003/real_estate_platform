import pandas as pd
import numpy as np
import os
import random
from datetime import timedelta

# File paths
DEALS_FILE = "data/processed/deals.csv"
OUTPUT_FILE = "data/processed/payment_plans.csv"

# Load deals
df_deals = pd.read_csv(DEALS_FILE)

# For reproducibility
random.seed(42)
np.random.seed(42)

payment_plans = []

for _, deal in df_deals.iterrows():
    deal_id = deal["id"]
    base_amount = deal["booking_price"]
    exit_date = pd.to_datetime(deal["planned_exit_date"], errors="coerce")

    if pd.isnull(exit_date):
        continue  # skip deals with no exit date

    # 1. Booking payment
    payment_plans.append({
        "deal_id": deal_id,
        "due_date": exit_date - timedelta(days=720),
        "amount": round(base_amount, 2),
        "payment_type": "booking",
        "is_paid": False
    })

    # 2. 4 installments between booking and handover
    for i in range(1, 5):
        due_date = exit_date - timedelta(days=540 - (i * 90))
        amount = round(np.random.uniform(50000, 200000), 2)
        payment_plans.append({
            "deal_id": deal_id,
            "due_date": due_date,
            "amount": amount,
            "payment_type": "installment",
            "is_paid": False
        })

    # 3. Handover payment
    payment_plans.append({
        "deal_id": deal_id,
        "due_date": exit_date,
        "amount": round(np.random.uniform(100000, 300000), 2),
        "payment_type": "handover",
        "is_paid": False
    })

# Convert to DataFrame
df_payments = pd.DataFrame(payment_plans)

# Add unique IDs
df_payments.reset_index(inplace=True)
df_payments.rename(columns={"index": "id"}, inplace=True)

# Save
os.makedirs("data/processed", exist_ok=True)
df_payments.to_csv(OUTPUT_FILE, index=False)

print(f"Saved payment plans to {OUTPUT_FILE}")
