import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
sns.set_theme(style="whitegrid")

months = pd.date_range("1841-01-01", "1846-12-31", freq="ME")
n = len(months)

clinic1_before = np.random.beta(2, 20, n // 2) * 15 + 5
clinic2_before = np.random.beta(1.5, 25, n // 2) * 15 + 4

handwashing_start = n // 2
clinic1_after = np.random.beta(1, 40, n - handwashing_start) * 8 + 1
clinic2_after = np.random.beta(1.5, 25, n - handwashing_start) * 15 + 4

clinic1_rates = np.concatenate([clinic1_before, clinic1_after])
clinic2_rates = np.concatenate([clinic2_before, clinic2_after])

df = pd.DataFrame({
    "date": months,
    "Clinic_1": clinic1_rates,
    "Clinic_2": clinic2_rates,
})

df["before_handwashing"] = df.index < handwashing_start

print("=" * 60)
print("HANDWASHING DISCOVERY: STATISTICAL ANALYSIS")
print("=" * 60)
print("\nDr. Semmelweis (1847): Handwashing reduces maternal mortality\n")

# Split data
c1_before = df[df["before_handwashing"]]["Clinic_1"]
c1_after = df[~df["before_handwashing"]]["Clinic_1"]
c2_before = df[df["before_handwashing"]]["Clinic_2"]
c2_after = df[~df["before_handwashing"]]["Clinic_2"]

print("--- Descriptive Statistics ---")
print(f"\nClinic 1 BEFORE handwashing: mean={c1_before.mean():.2f}%, std={c1_before.std():.2f}")
print(f"Clinic 1 AFTER handwashing:  mean={c1_after.mean():.2f}%, std={c1_after.std():.2f}")
print(f"Reduction: {c1_before.mean() - c1_after.mean():.2f} percentage points")

# t-tests
print("\n--- Independent t-Tests ---")
t1, p1 = stats.ttest_ind(c1_before, c2_before)
print(f"Clinic 1 vs Clinic 2 (before): t={t1:.3f}, p={p1:.4f} {'SIGNIFICANT' if p1 < 0.05 else 'NOT SIGNIFICANT'}")

t2, p2 = stats.ttest_ind(c1_before, c1_after)
print(f"Clinic 1 before vs after:       t={t2:.3f}, p={p2:.6f} {'SIGNIFICANT' if p2 < 0.05 else 'NOT SIGNIFICANT'}")

t3, p3 = stats.ttest_ind(c2_before, c2_after)
print(f"Clinic 2 before vs after:       t={t3:.3f}, p={p3:.4f} {'SIGNIFICANT' if p3 < 0.05 else 'NOT SIGNIFICANT'}")

t4, p4 = stats.ttest_ind(c1_after, c2_after)
print(f"Clinic 1 vs Clinic 2 (after):  t={t4:.3f}, p={p4:.4f} {'SIGNIFICANT' if p4 < 0.05 else 'NOT SIGNIFICANT'}")

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("The Semmelweis Discovery: Handwashing Reduces Mortality", fontsize=14, fontweight="bold")

ax1 = axes[0, 0]
sns.histplot(c1_before, kde=True, color="red", alpha=0.5, label="Clinic 1 (Before)", ax=ax1, bins=15)
sns.histplot(c1_after, kde=True, color="green", alpha=0.5, label="Clinic 1 (After)", ax=ax1, bins=15)
ax1.set_title("Clinic 1: Mortality Distribution Before vs After")
ax1.set_xlabel("Mortality Rate (%)")
ax1.legend()

ax2 = axes[0, 1]
box_data = pd.DataFrame({
    "Clinic 1 Before": c1_before.values,
    "Clinic 1 After": c1_after.values,
    "Clinic 2 Before": c2_before.values,
    "Clinic 2 After": c2_after.values,
})
sns.boxplot(data=box_data, palette=["#e74c3c", "#2ecc71", "#e74c3c", "#2ecc71"], ax=ax2)
ax2.set_title("Mortality Rate Comparison")
ax2.set_ylabel("Mortality Rate (%)")
ax2.tick_params(axis="x", rotation=30)

ax3 = axes[1, 0]
rolling1 = df["Clinic_1"].rolling(window=6).mean()
rolling2 = df["Clinic_2"].rolling(window=6).mean()
ax3.plot(df["date"], rolling1, label="Clinic 1", color="#e74c3c", linewidth=2)
ax3.plot(df["date"], rolling2, label="Clinic 2", color="#3498db", linewidth=2)
ax3.axvline(months[handwashing_start], color="green", linestyle="--", linewidth=2, label="Handwashing introduced")
ax3.set_title("6-Month Rolling Average Mortality")
ax3.set_ylabel("Mortality Rate (%)")
ax3.legend()

ax4 = axes[1, 1]
means = [c1_before.mean(), c1_after.mean(), c2_before.mean(), c2_after.mean()]
errors = [c1_before.std(), c1_after.std(), c2_before.std(), c2_after.std()]
labels = ["C1 Before", "C1 After", "C2 Before", "C2 After"]
colors = ["#e74c3c", "#2ecc71", "#e74c3c", "#3498db"]
bars = ax4.bar(labels, means, yerr=errors, color=colors, capsize=5)
ax4.set_title("Mean Mortality Rate ± 1 SD")
ax4.set_ylabel("Mortality Rate (%)")

plt.tight_layout()
plt.savefig("Day079/handwashing_analysis.png", dpi=150, bbox_inches="tight")
print("\nChart saved to Day079/handwashing_analysis.png")
plt.close()

df.to_csv("Day079/mortality_data.csv", index=False)
print("Data saved to Day079/mortality_data.csv")
