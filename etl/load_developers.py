import pandas as pd
import os

# Define a synthetic list of developers
developers = [
    {
        "id": 1,
        "name": "Aldar Properties",
        "tier": 1,
        "track_record_score": 92,
        "projects_completed": 125,
        "on_time_completion_rate": 95.2
    },
    {
        "id": 2,
        "name": "Reportage",
        "tier": 2,
        "track_record_score": 73,
        "projects_completed": 28,
        "on_time_completion_rate": 82.0
    },
    {
        "id": 3,
        "name": "Imkan",
        "tier": 1,
        "track_record_score": 89,
        "projects_completed": 18,
        "on_time_completion_rate": 91.4
    },
    {
        "id": 4,
        "name": "Bloom Holding",
        "tier": 2,
        "track_record_score": 80,
        "projects_completed": 20,
        "on_time_completion_rate": 87.3
    },
    {
        "id": 5,
        "name": "Tiger Properties",
        "tier": 3,
        "track_record_score": 65,
        "projects_completed": 16,
        "on_time_completion_rate": 75.0
    }
]

# Convert to DataFrame
df = pd.DataFrame(developers)

# Save to CSV
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/developers.csv", index=False)

print("Saved developers to data/processed/developers.csv")
