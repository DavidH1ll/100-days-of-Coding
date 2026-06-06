import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

np.random.seed(42)
sns.set_theme(style="whitegrid")

n_incidents = 8000
years = np.random.randint(2000, 2023, n_incidents)
states = [f"State_{i}" for i in range(1, 51)]
races = ["White", "Black", "Hispanic", "Asian", "Native American", "Other"]
circumstances = ["Traffic Stop", "Domestic Disturbance", "Mental Health Crisis",
                 "Armed Robbery", "Assault", "Investigation", "Warrant Service",
                 "Drug-related", "Other Violent Crime", "Non-violent Offense",
                 "Suicide Prevention", "Barricaded Subject", "Stolen Vehicle",
                 "Suspicious Person", "Active Shooter"]
armed_status = ["Firearm", "Knife", "Vehicle", "Unarmed", "Toy/Replica", "Other Weapon", "Undetermined"]

data = {
    "date": pd.to_datetime([f"{y}-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}" for y in years]),
    "state": np.random.choice(states, n_incidents, p=[0.04]*10 + [0.02]*10 + [0.01]*30),
    "race": np.random.choice(races, n_incidents, p=[0.45, 0.25, 0.16, 0.05, 0.03, 0.06]),
    "age": np.clip(np.random.normal(35, 12, n_incidents), 15, 80).astype(int),
    "gender": np.random.choice(["Male", "Female"], n_incidents, p=[0.94, 0.06]),
    "circumstance": np.random.choice(circumstances, n_incidents),
    "armed": np.random.choice(armed_status, n_incidents, p=[0.35, 0.10, 0.05, 0.15, 0.05, 0.15, 0.15]),
}
df = pd.DataFrame(data)
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

print("=" * 60)
print("POLICE-INVOLVED DEATHS ANALYSIS (2000-2022)")
print("=" * 60)
print(f"Total incidents: {len(df)}")
print(f"Year range: {df['year'].min()}-{df['year'].max()}")

# 1. Deaths by state
fig, ax = plt.subplots(figsize=(14, 6))
state_counts = df["state"].value_counts()
ax.bar(range(len(state_counts)), state_counts.values, color="steelblue")
ax.set_title("Incidents by State", fontsize=14)
ax.set_xlabel("State (anonymized)")
ax.set_ylabel("Number of Incidents")
plt.tight_layout()
plt.savefig("Day099/deaths_by_state.png", dpi=150)
print("Saved: deaths_by_state.png")
plt.close()

# 2. Race distribution
fig, ax = plt.subplots(figsize=(8, 8))
race_counts = df["race"].value_counts()
ax.pie(race_counts, labels=race_counts.index, autopct="%1.1f%%",
       colors=sns.color_palette("Set2"), startangle=90)
ax.set_title("Distribution by Race/Ethnicity", fontsize=14)
plt.tight_layout()
plt.savefig("Day099/race_distribution.png", dpi=150)
print("Saved: race_distribution.png")
plt.close()

# 3. Time series
fig, ax = plt.subplots(figsize=(12, 6))
yearly = df.groupby("year").size()
ax.plot(yearly.index, yearly.values, marker="o", linewidth=2, color="#e74c3c")
z = np.polyfit(yearly.index, yearly.values, 1)
trend = np.poly1d(z)
ax.plot(yearly.index, trend(yearly.index), "--", color="gray", label="Trend")
ax.set_title("Incidents Over Time", fontsize=14)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Incidents")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Day099/time_series.png", dpi=150)
print("Saved: time_series.png")
plt.close()

# 4. Circumstances
fig, ax = plt.subplots(figsize=(10, 8))
circ_counts = df["circumstance"].value_counts().sort_values()
ax.barh(circ_counts.index, circ_counts.values, color="steelblue")
ax.set_title("Incidents by Circumstance", fontsize=14)
ax.set_xlabel("Number of Incidents")
plt.tight_layout()
plt.savefig("Day099/by_circumstance.png", dpi=150)
print("Saved: by_circumstance.png")
plt.close()

# 5. Age distribution
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["age"], bins=25, kde=True, color="#3498db", ax=ax)
ax.set_title("Age Distribution", fontsize=14)
ax.set_xlabel("Age")
plt.tight_layout()
plt.savefig("Day099/age_distribution.png", dpi=150)
print("Saved: age_distribution.png")
plt.close()

# 6. Heatmap: state × year
heatmap_data = df.pivot_table(index="state", columns="year", aggfunc="size", fill_value=0)
fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(heatmap_data.iloc[:20], cmap="YlOrRd", ax=ax)
ax.set_title("Incidents Heatmap: Top 20 States × Year", fontsize=14)
plt.tight_layout()
plt.savefig("Day099/heatmap.png", dpi=150)
print("Saved: heatmap.png")
plt.close()

# 7. Armed status
fig, ax = plt.subplots(figsize=(8, 8))
armed_counts = df["armed"].value_counts()
ax.pie(armed_counts, labels=armed_counts.index, autopct="%1.1f%%",
       colors=sns.color_palette("Set3"), startangle=90)
ax.set_title("Armed Status Distribution", fontsize=14)
plt.tight_layout()
plt.savefig("Day099/armed_status.png", dpi=150)
print("Saved: armed_status.png")
plt.close()

# Chi-square test
print("\n--- Chi-Square Test: Race vs Armed Status ---")
contingency = pd.crosstab(df["race"], df["armed"])
chi2, p, dof, expected = chi2_contingency(contingency)
print(f"Chi²: {chi2:.2f}")
print(f"p-value: {p:.6f}")
print(f"Significant: {'Yes' if p < 0.05 else 'No'} (α=0.05)")

df.to_csv("Day099/police_deaths.csv", index=False)
print("\nData saved to Day099/police_deaths.csv")
