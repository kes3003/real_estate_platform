import pandas as pd
import numpy as np
import os
from datetime import timedelta
from datetime import datetime
import random

# Input
PROJECTS_FILE = "data/processed/projects.csv"
OUTPUT_FILE = "data/processed/deals.csv"

# Load project data
df_projects = pd.read_csv(PROJECTS_FILE)

# Define strategies
strategies = ["offplan_flip", "handover_flip", "hold_and_rent"]

# For reproducibility
random.seed(42)
np.random.seed(42)

deals = []

for _, row in df_projects.iterrows():
    project_id = row["id"]
    unit_type = row["unit_type"] if pd.notnull(row["unit_type"]) else "1 bed"
    base_price = row["base_price"]

    # Booking = 5% to 15% of base
    booking_price = round(base_price * np.random.uniform(0.05, 0.15), 2)

    # Flip price = 15% to 40% higher than base
    expected_flip_price = round(base_price * np.random.uniform(1.15, 1.40), 2)

    # Random strategy
    strategy = random.choice(strategies)

    # Random exit date between launch and handover
    try:
        launch = pd.to_datetime(f"{int(row['launch_year'])}-01-01", errors="coerce")
        handover = pd.to_datetime(row["handover_date"], errors="coerce")
        if pd.notnull(launch) and pd.notnull(handover):
            exit_date = launch + timedelta(
                days=random.randint(180, int((handover - launch).days))
            )
        else:
            exit_date = pd.NaT
    except:
        exit_date = pd.NaT

    deals.append({
        "project_id": project_id,
        "unit_type": unit_type,
        "booking_price": booking_price,
        "expected_flip_price": expected_flip_price,
        "strategy": strategy,
        "planned_exit_date": exit_date.date() if pd.notnull(exit_date) else None
    })

# Convert to DataFrame
df_deals = pd.DataFrame(deals)

# Add unique deal IDs
df_deals.reset_index(inplace=True)
df_deals.rename(columns={"index": "id"}, inplace=True)

# Save to file
os.makedirs("data/processed", exist_ok=True)
df_deals.to_csv(OUTPUT_FILE, index=False)

print(f"Saved deals to {OUTPUT_FILE}")
