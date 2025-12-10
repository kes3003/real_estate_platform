import pandas as pd
import numpy as np
import os

# File paths
RAW_DATA = "data/processed/cleaned_adrec_full.csv"
AREAS_DATA = "data/processed/areas.csv"
OUTPUT_FILE = "data/processed/market_history.csv"

# Load data
df_raw = pd.read_csv(RAW_DATA)
df_areas = pd.read_csv(AREAS_DATA)

# Drop nulls for needed fields
df = df_raw.dropna(subset=["Community", "Rate (AED/sqm)", "Registration"]).copy()

# Extract year
df["year"] = pd.to_datetime(df["Registration"], errors='coerce').dt.year

# Join to get area_id
df = df.merge(
    df_areas[["name"]].reset_index().rename(columns={"index": "area_id"}),
    left_on="Community",
    right_on="name",
    how="left"
)

# Drop unmatched areas
df = df.dropna(subset=["area_id"])
df["area_id"] = df["area_id"].astype(int)

# Group by area and year
grouped = df.groupby(["area_id", "year"]).agg({
    "Rate (AED/sqm)": "mean"
}).reset_index()

# Clean column names
grouped.rename(columns={"Rate (AED/sqm)": "avg_price_per_sqm"}, inplace=True)
grouped["avg_price_per_sqm"] = grouped["avg_price_per_sqm"].round(2)

# Sort for growth calc
grouped = grouped.sort_values(by=["area_id", "year"])

# Compute YOY growth
grouped["growth_rate"] = grouped.groupby("area_id")["avg_price_per_sqm"].pct_change() * 100
grouped["growth_rate"] = grouped["growth_rate"].round(2)

# Data quality filters
grouped["growth_rate"] = grouped["growth_rate"].clip(upper=300)
grouped = grouped[grouped["avg_price_per_sqm"] >= 500]
grouped = grouped.replace([np.inf, -np.inf], np.nan).dropna(subset=["growth_rate"])

# Reset index to expose area_id
df_areas = df_areas.reset_index().rename(columns={"index": "area_id"})

# Compute average rental yield from min and max
df_areas["avg_rental_yield"] = (
    df_areas["rental_yield_min"] + df_areas["rental_yield_max"]
) / 2

# Map average rental yield to market history by area_id
rental_yield_map = df_areas.reset_index().set_index("index")["avg_rental_yield"].to_dict()
grouped["avg_rental_yield"] = grouped["area_id"].map(rental_yield_map)

# Calculate estimated monthly rent per sqm
grouped["avg_rent_per_sqm"] = (
    (grouped["avg_price_per_sqm"] * grouped["avg_rental_yield"]) / 100 / 12
).round(2)

# Drop temporary column
grouped.drop(columns=["avg_rental_yield"], inplace=True)

# Add auto-incremented ID
grouped.reset_index(drop=True, inplace=True)
grouped["id"] = grouped.index

# Reorder columns to match schema
grouped = grouped[["id", "area_id", "year", "avg_price_per_sqm", "growth_rate", "avg_rent_per_sqm"]]

# Save to CSV
os.makedirs("data/processed", exist_ok=True)
grouped.to_csv(OUTPUT_FILE, index=False)

print(f"Saved market history to {OUTPUT_FILE}")
