import pandas as pd
import numpy as np
import os

# File paths
INPUT_FILE = "data/processed/cleaned_adrec_full.csv"
OUTPUT_FILE = "data/processed/areas.csv"

# Load cleaned dataset
df = pd.read_csv(INPUT_FILE)

# Drop rows with missing Community or Rate columns
df = df.dropna(subset=["Community", "Rate (AED/sqm)"])

# Group by Community
grouped = df.groupby("Community").agg({
    "District": "first",
    "Rate (AED/sqm)": "mean"
}).reset_index()

# Rename columns to match schema
grouped.rename(columns={
    "Community": "name",
    "District": "district",  
    "Rate (AED/sqm)": "avg_price_per_sqm"
}, inplace=True)

# Round avg price
grouped["avg_price_per_sqm"] = grouped["avg_price_per_sqm"].round(2)

# Add synthetic area type
grouped["type"] = np.random.choice(["island", "city", "waterfront", "suburb"], size=len(grouped))

# Add synthetic price growth
grouped["past_growth_rate"] = np.round(np.random.uniform(2.0, 6.0, len(grouped)), 2)

# Add synthetic rental yield range
base_yield = np.round(np.random.uniform(5.0, 7.0, len(grouped)), 2)
grouped["rental_yield_min"] = base_yield - 0.5
grouped["rental_yield_max"] = base_yield + 0.5

# Add synthetic liquidity score
grouped["liquidity_score"] = np.round(np.random.uniform(30, 90, len(grouped)), 2)

# Final column selection
final_cols = [
    "name", "type", "avg_price_per_sqm", "past_growth_rate",
    "rental_yield_min", "rental_yield_max", "liquidity_score"
]
grouped = grouped[final_cols]

# Save to CSV
os.makedirs("data/processed", exist_ok=True)
grouped.to_csv(OUTPUT_FILE, index=False)

print(f"Saved processed area data to {OUTPUT_FILE}")

