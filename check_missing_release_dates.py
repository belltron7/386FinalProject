import json
import pandas as pd

with open("movies.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Show how many rows actually have a non-null release_date
has_release_date = df['release_date'].notna().sum()
total = len(df)

print(f"Movies with release_date: {has_release_date} / {total}")
print(df['release_date'].value_counts(dropna=False).head(10))  # See what it looks like
