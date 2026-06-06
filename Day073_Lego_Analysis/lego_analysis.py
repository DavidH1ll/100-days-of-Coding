import pandas as pd
import numpy as np

np.random.seed(42)

n_sets = 77
themes_list = [
    "City", "Star Wars", "Creator", "Technic", "Friends",
    "Ninjago", "Harry Potter", "Marvel", "DC", "Classic",
    "Architecture", "Minecraft", "Duplo", "Ideas", "Speed Champions"
]

themes_df = pd.DataFrame({
    "theme_id": range(1, len(themes_list) + 1),
    "theme_name": themes_list,
    "licensed": [t in ["Star Wars", "Harry Potter", "Marvel", "DC", "Minecraft"] for t in themes_list]
})

sets_data = {
    "set_id": range(1, n_sets + 1),
    "theme_id": np.random.choice(themes_df["theme_id"], n_sets),
    "year": np.random.randint(1978, 2024, n_sets),
    "pieces": np.random.randint(10, 5500, n_sets),
    "price_usd": np.round(np.random.uniform(4.99, 499.99, n_sets), 2),
}

sets_df = pd.DataFrame(sets_data)
sets_df.loc[np.random.choice(n_sets, 3, replace=False), "price_usd"] = np.nan

print("=" * 60)
print("LEGO DATASET ANALYSIS")
print("=" * 60)

print("\n--- Sets DataFrame head ---")
print(sets_df.head())

print("\n--- Themes DataFrame ---")
print(themes_df)

merged = sets_df.merge(themes_df, on="theme_id")
print(f"\n--- Merged shape: {merged.shape} ---")

print("\n--- Average pieces per year ---")
yearly = merged.groupby("year").agg(
    avg_pieces=("pieces", "mean"),
    avg_price=("price_usd", "mean"),
    set_count=("set_id", "count")
).round(1)
print(yearly.head(10))

print("\n--- Top 5 themes by set count ---")
theme_counts = merged["theme_name"].value_counts().head()
print(theme_counts)

print("\n--- Licensed vs Non-Licensed ---")
licensed_stats = merged.groupby("licensed").agg(
    avg_pieces=("pieces", "mean"),
    avg_price=("price_usd", "mean"),
    set_count=("set_id", "count")
).round(1)
print(licensed_stats)

print("\n--- Most expensive sets ---")
print(merged.nlargest(5, "price_usd")[["set_id", "theme_name", "year", "price_usd", "pieces"]])

pivot = merged.pivot_table(
    values="set_id", index="theme_name", columns="year", aggfunc="count", fill_value=0
)
print(f"\n--- Pivot table shape: {pivot.shape} ---")

sets_df.to_csv("Day073/lego_sets.csv", index=False)
themes_df.to_csv("Day073/lego_themes.csv", index=False)
print("\nData saved to Day073/lego_sets.csv and lego_themes.csv")
