import json
import pandas as pd

# === Load Data ===
with open("movies.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# === Parse and Filter Years ===
df = df[df['release_date'].notna()]
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df = df[df['release_date'].notna()]
df['year'] = df['release_date'].dt.year

# === Show Distribution ===
year_counts = df['year'].value_counts().sort_index()
print("Movie counts by year:")
print(year_counts)
