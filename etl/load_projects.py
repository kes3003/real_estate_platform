import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# File paths
RAW_DATA = "data/processed/cleaned_adrec_full.csv"
AREAS_DATA = "data/processed/areas.csv"
OUTPUT_FILE = "data/processed/projects.csv"

# Load input files
df_raw = pd.read_csv(RAW_DATA)
df_areas = pd.read_csv(AREAS_DATA)

# Drop rows missing required fields
df = df_raw.dropna(subset=[
    "Project", "Community", "Price (AED)", "Sold Area / GFA (sqm)", "Sale Type", "Registration"
])

# Deduplicate projects (by name + community)
df = df.drop_duplicates(subset=["Project", "Community"])

# Join with areas to get area_id (based on Community)
df = df.merge(
    df_areas[["name"]].reset_index().rename(columns={"index": "area_id"}),
    left_on="Community",
    right_on="name",
    how="left"
)

# Drop unmatched areas
df = df.dropna(subset=["area_id"])
df["area_id"] = df["area_id"].astype(int)

# Temporary synthetic developer_id (random from 1 to 5)
df["developer_id"] = np.random.randint(1, 6, size=len(df))

# Clean unit type using Layout or Property Type
df["unit_type"] = df["Layout"].fillna(df["Property Type"]).str.strip()

# Normalize price and size
df["base_price"] = df["Price (AED)"].astype(float).round(2)
df["avg_unit_size_sqm"] = df["Sold Area / GFA (sqm)"].astype(float).round(1)

# Normalize status from Sale Type
def classify_status(sale_type):
    val = str(sale_type).lower()
    if "off" in val:
        return "off_plan"
    elif "ready" in val:
        return "completed"
    elif "court" in val:
        return "court_mandated"
    else:
        return "other"

df["status"] = df["Sale Type"].apply(classify_status)

# Launch year is 1–2 years before registration
df["launch_year"] = pd.to_datetime(df["Registration"], errors='coerce').dt.year - np.random.randint(1, 3, size=len(df))

# Handover date = launch + 2 years ± random offset (0–6 months)
df["handover_date"] = pd.to_datetime(df["launch_year"], format="%Y") + pd.DateOffset(years=2)
df["handover_date"] = df["handover_date"] + pd.to_timedelta(np.random.randint(0, 180, len(df)), unit='D')

# Select and rename final columns
projects = df[[
    "Project", "area_id", "developer_id", "unit_type",
    "base_price", "avg_unit_size_sqm", "status",
    "launch_year", "handover_date"
]].rename(columns={"Project": "name"})

projects.reset_index(drop=True, inplace=True)
projects.insert(0, "id", projects.index)

# Save to CSV
os.makedirs("data/processed", exist_ok=True)
projects.to_csv(OUTPUT_FILE, index=False)
print(f" Saved projects to {OUTPUT_FILE}")
