import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)

countries = ["USA", "USSR/Russia", "China", "France", "Japan", "India",
             "UK", "Germany", "Canada", "Italy", "South Korea", "Brazil"]
mission_types = ["Satellite", "Crewed", "Lunar", "Mars", "Probe", "Telescope",
                 "Cargo", "Test Flight", "Interplanetary"]
n_missions = 5000
years = np.random.randint(1957, 2021, n_missions)

data = {
    "year": years,
    "country": np.random.choice(countries, n_missions, p=[0.35, 0.25, 0.08, 0.06, 0.05, 0.04, 0.04, 0.03, 0.02, 0.02, 0.02, 0.02]),
    "mission_type": np.random.choice(mission_types, n_missions, p=[0.30, 0.05, 0.10, 0.08, 0.15, 0.05, 0.10, 0.07, 0.10]),
    "success": np.random.choice([True, False], n_missions, p=[0.88, 0.12]),
    "cost_millions": np.round(np.random.uniform(10, 5000, n_missions), 1),
}
df = pd.DataFrame(data)

print("=" * 60)
print("SPACE RACE ANALYSIS (1957-2020)")
print("=" * 60)
print(f"Total missions: {len(df)}")
print(f"Success rate: {df['success'].mean()*100:.1f}%")
print(f"Total cost: ${df['cost_millions'].sum():,.0f}M")

# 1. Missions per year
fig, ax = plt.subplots(figsize=(12, 6))
yearly = df.groupby("year").size()
ax.fill_between(yearly.index, yearly.values, alpha=0.5, color="#3498db")
ax.plot(yearly.index, yearly.values, color="#2980b9", linewidth=2)
ax.set_title("Space Missions per Year", fontsize=14)
ax.set_xlabel("Year")
ax.set_ylabel("Missions")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Day098/missions_per_year.png", dpi=150)
print("Saved: missions_per_year.png")
plt.close()

# 2. Success rate over time
fig, ax = plt.subplots(figsize=(12, 6))
success_rate = df.groupby(df["year"] // 5 * 5)["success"].mean() * 100
ax.bar(success_rate.index, success_rate.values, width=3, color="#2ecc71", edgecolor="white")
ax.set_title("Mission Success Rate (5-Year Windows)", fontsize=14)
ax.set_xlabel("Year")
ax.set_ylabel("Success Rate (%)")
ax.set_ylim(60, 100)
ax.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig("Day098/success_rate.png", dpi=150)
print("Saved: success_rate.png")
plt.close()

# 3. Missions by country (Plotly choropleth)
country_counts = df.groupby("country").size().reset_index(name="missions")
fig = px.choropleth(country_counts, locations="country", locationmode="country names",
                    color="missions", title="Space Missions by Country",
                    color_continuous_scale="Blues")
fig.write_html("Day098/choropleth.html")
print("Saved: choropleth.html")

# 4. Mission types (Plotly sunburst)
fig = px.sunburst(df, path=["country", "mission_type"], title="Mission Types by Country",
                  color_discrete_sequence=px.colors.qualitative.Set3)
fig.write_html("Day098/sunburst.html")
print("Saved: sunburst.html")

# 5. Cost analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
avg_cost = df.groupby("country")["cost_millions"].mean().sort_values(ascending=False)
axes[0].barh(avg_cost.index, avg_cost.values, color="steelblue")
axes[0].set_title("Average Mission Cost by Country ($M)")
axes[0].set_xlabel("Cost ($M)")

cost_over_time = df.groupby(df["year"] // 5 * 5)["cost_millions"].mean()
axes[1].plot(cost_over_time.index, cost_over_time.values, marker="o", linewidth=2, color="#e74c3c")
axes[1].set_title("Average Mission Cost Over Time")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Cost ($M)")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Day098/cost_analysis.png", dpi=150)
print("Saved: cost_analysis.png")
plt.close()

df.to_csv("Day098/space_missions.csv", index=False)
print("Data saved to Day098/space_missions.csv")
print("\nAnalysis complete!")
