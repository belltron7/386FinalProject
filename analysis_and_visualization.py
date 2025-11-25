import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === Load Data ===
with open("movies.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# === Clean & Prepare ===
df = pd.DataFrame(data)
df = df[df['release_date'].notna()]
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df = df[df['release_date'].notna()]
df['year'] = df['release_date'].dt.year
df = df[df['year'].between(2005, 2025)]

df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
df['profit'] = df['revenue'] - df['budget']
df['year'] = df['release_date'].dt.year

# === Summary Stats ===
print("=== Summary Stats ===")
print("Total movies:", len(df))
print("Average budget:", df['budget'].mean())
print("Average revenue:", df['revenue'].mean())
print("Average profit:", df['profit'].mean())

# === Profit Over Time (Fixed) ===
yearly = (
    df.groupby('year')[['budget', 'revenue', 'profit']]
    .mean()
    .reset_index()
)

# Drop years with missing or zero values
yearly = yearly[yearly['profit'].notna()]
yearly = yearly[yearly['profit'] > 0]

print("Yearly profit data:")
print(yearly)

plt.figure(figsize=(10, 5))
sns.lineplot(data=yearly, x='year', y='profit', marker='o')
plt.title('Average Profit by Year')
plt.xlabel('Year')
plt.ylabel('Average Profit')
plt.grid(True)
plt.tight_layout()
plt.show()

print(df['year'].value_counts().sort_index())

# === Profit by Genre ===
def extract_genres(genre_list):
    return [g['name'] for g in genre_list] if isinstance(genre_list, list) else []

df['genre_list'] = df['genres'].apply(extract_genres)
df_genres = df.explode('genre_list')

genre_profit = df_genres.groupby('genre_list')['profit'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=genre_profit.values, y=genre_profit.index)
plt.title("Average Profit by Genre")
plt.xlabel("Average Profit")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()

# === Profit by Production Company ===
def extract_companies(company_list):
    return [c['name'] for c in company_list] if isinstance(company_list, list) else []

df['company_list'] = df['production_companies'].apply(extract_companies)
df_companies = df.explode('company_list')

company_profit = (
    df_companies.groupby('company_list')['profit']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
sns.barplot(x=company_profit.values, y=company_profit.index)
plt.title("Top 10 Production Companies by Average Profit")
plt.xlabel("Average Profit")
plt.ylabel("Production Company")
plt.tight_layout()
plt.show()
