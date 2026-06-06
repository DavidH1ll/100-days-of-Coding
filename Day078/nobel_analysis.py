import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

np.random.seed(42)
sns.set_theme(style="whitegrid")

n = 950
categories = ["Physics", "Chemistry", "Medicine", "Literature", "Peace", "Economics"]
countries = ["USA", "UK", "Germany", "France", "Sweden", "Japan", "Russia", "China", "India", "Canada",
             "Switzerland", "Netherlands", "Italy", "Australia", "Poland", "Norway", "Denmark", "Austria", "Belgium", "Israel"]
genders = ["Male", "Female"]

data = {
    "year": np.random.randint(1901, 2024, n),
    "category": np.random.choice(categories, n),
    "country": np.random.choice(countries, n, p=[0.25, 0.12, 0.10, 0.08, 0.06, 0.05, 0.05, 0.04, 0.03, 0.03] +
                                            [0.02]*10),
    "gender": np.random.choice(genders, n, p=[0.82, 0.18]),
    "age": np.random.randint(30, 90, n),
    "name": [f"Laureate_{i}" for i in range(n)],
}
df = pd.DataFrame(data)

print("=" * 60)
print("NOBEL PRIZE ANALYSIS")
print("=" * 60)
print(f"Total laureates: {len(df)}")
print(f"Year range: {df['year'].min()}-{df['year'].max()}")
print(f"Categories: {df['category'].nunique()}")
print(f"Countries represented: {df['country'].nunique()}")

# 1. Prizes over time by category
fig, ax = plt.subplots(figsize=(12, 6))
decade_counts = df.groupby([df["year"] // 10 * 10, "category"]).size().unstack(fill_value=0)
decade_counts.plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
ax.set_title("Nobel Prizes by Decade and Category", fontsize=14)
ax.set_xlabel("Decade")
ax.set_ylabel("Number of Prizes")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig("Day078/nobel_decades.png", dpi=150, bbox_inches="tight")
print("Saved: nobel_decades.png")
plt.close()

# 2. Choropleth
country_counts = df["country"].value_counts().reset_index()
country_counts.columns = ["country", "prizes"]
fig = px.choropleth(
    country_counts, locations="country", locationmode="country names",
    color="prizes", title="Nobel Prizes by Country",
    color_continuous_scale="Blues"
)
fig.write_html("Day078/choropleth.html")
print("Saved: choropleth.html")

# 3. Sunburst
fig = px.sunburst(
    df, path=["category", "gender"], title="Prizes by Category and Gender",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.write_html("Day078/sunburst.html")
print("Saved: sunburst.html")

# 4. Age distribution + gender
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for gender in genders:
    subset = df[df["gender"] == gender]
    axes[0].hist(subset["age"], alpha=0.6, label=gender, bins=20)
axes[0].set_title("Age Distribution by Gender")
axes[0].set_xlabel("Age")
axes[0].legend()

# 5. Donut chart for gender
gender_counts = df["gender"].value_counts()
axes[1].pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%",
            colors=["#3498db", "#e84393"], startangle=90,
            wedgeprops={"width": 0.4})
axes[1].set_title("Gender Distribution")

plt.tight_layout()
plt.savefig("Day078/nobel_demographics.png", dpi=150, bbox_inches="tight")
print("Saved: nobel_demographics.png")
plt.close()

# 6. Top countries bar
fig, ax = plt.subplots(figsize=(10, 6))
top10 = country_counts.head(10)
sns.barplot(data=top10, x="prizes", y="country", palette="Blues_r", ax=ax)
ax.set_title("Top 10 Countries by Nobel Prizes")
plt.tight_layout()
plt.savefig("Day078/top_countries.png", dpi=150, bbox_inches="tight")
print("Saved: top_countries.png")
plt.close()

df.to_csv("Day078/nobel_prizes.csv", index=False)
print("Data saved to Day078/nobel_prizes.csv")
