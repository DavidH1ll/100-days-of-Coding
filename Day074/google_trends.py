import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range("2022-01-01", "2023-12-31", freq="D")
n = len(dates)

topics = {
    "Python": {"base": 50, "trend": 0.03, "amplitude": 15, "phase": 0},
    "Machine Learning": {"base": 35, "trend": 0.04, "amplitude": 10, "phase": 60},
    "Web Development": {"base": 40, "trend": -0.01, "amplitude": 8, "phase": 120},
}

df = pd.DataFrame({"date": dates})
for topic, params in topics.items():
    day_num = np.arange(n)
    seasonal = params["amplitude"] * np.sin(2 * np.pi * (day_num + params["phase"]) / 365)
    trend = params["trend"] * day_num
    noise = np.random.normal(0, 5, n)
    df[topic] = np.clip(params["base"] + trend + seasonal + noise, 0, 100)

df.set_index("date", inplace=True)

print("=" * 60)
print("GOOGLE TRENDS: TIME SERIES ANALYSIS")
print("=" * 60)

print("\n--- First 5 days ---")
print(df.head())

weekly = df.resample("W").mean()
monthly = df.resample("ME").mean()
quarterly = df.resample("QE").mean()

print(f"\nDaily: {len(df)} rows")
print(f"Weekly: {len(weekly)} rows")
print(f"Monthly: {len(monthly)} rows")
print(f"Quarterly: {len(quarterly)} rows")

print("\n--- Monthly averages (first 6 months) ---")
print(monthly.head(6).round(1))

rolling_30 = df.rolling(window=30).mean()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Google Trends: Time Series Analysis", fontsize=16, fontweight="bold")

ax1 = axes[0, 0]
for topic in topics:
    ax1.plot(monthly.index, monthly[topic], label=topic, linewidth=2)
ax1.set_title("Monthly Aggregated Trends")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2 = axes[0, 1]
for topic in topics:
    ax2.plot(rolling_30.index, rolling_30[topic], label=f"{topic} (30d avg)", linewidth=2)
ax2.set_title("30-Day Rolling Average")
ax2.legend()
ax2.grid(True, alpha=0.3)

ax3 = axes[1, 0]
df_2023 = df["2023"]
days_2023 = np.arange(len(df_2023))
for topic in topics:
    ax3.plot(days_2023, df_2023[topic], alpha=0.3, linewidth=0.5, color="gray" if topic == "Web Development" else None)
ax3.plot(days_2023, df_2023["Python"], label="Python (daily)", alpha=0.7, linewidth=1)
ax3.plot(days_2023, df_2023["Python"].rolling(7).mean(), label="Python (7d avg)", linewidth=2, color="red")
ax3.set_title("2023: Daily vs 7-Day Average (Python)")
ax3.legend()
ax3.grid(True, alpha=0.3)

ax4 = axes[1, 1]
python_by_day = df["Python"].groupby(df.index.dayofyear).mean()
ax4.plot(python_by_day.index, python_by_day.values, linewidth=2, color="#3776AB")
ax4.axhline(python_by_day.mean(), color="red", linestyle="--", label=f"Average: {python_by_day.mean():.1f}")
ax4.set_title("Average Python Interest by Day of Year")
ax4.set_xlabel("Day of Year")
ax4.set_ylabel("Average Interest")
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Day074/google_trends.png", dpi=150, bbox_inches="tight")
print("\nChart saved to Day074/google_trends.png")
plt.close()

df.to_csv("Day074/trend_data.csv")
print("Data saved to Day074/trend_data.csv")
