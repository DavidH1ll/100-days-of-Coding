import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

np.random.seed(42)

categories_list = ["Games", "Productivity", "Social", "Education", "Health", "Finance", "Music", "Travel"]
n_apps = 80

data = {
    "App": [f"App_{i}" for i in range(1, n_apps + 1)],
    "Category": np.random.choice(categories_list, n_apps),
    "Rating": np.round(np.clip(np.random.normal(4.0, 0.6, n_apps), 1.0, 5.0), 1),
    "Reviews": np.random.randint(50, 500000, n_apps),
    "Installs": [f"{x}+" for x in np.random.choice([1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000], n_apps)],
    "Price": np.where(np.random.random(n_apps) < 0.4, 0, np.round(np.random.uniform(0.99, 19.99, n_apps), 2)),
    "Size_MB": np.round(np.random.uniform(2, 250, n_apps), 1),
}

df = pd.DataFrame(data)
df["Free"] = df["Price"] == 0

print("=" * 60)
print("ANDROID APP STORE ANALYSIS WITH PLOTLY")
print("=" * 60)

print(f"\nTotal apps: {len(df)}")
print(f"Free apps: {df['Free'].sum()} ({df['Free'].mean()*100:.0f}%)")
print(f"Average rating: {df['Rating'].mean():.2f}")
print(f"Categories: {df['Category'].nunique()}")

fig1 = px.scatter(
    df, x="Reviews", y="Rating", color="Category", size="Size_MB",
    hover_data=["App", "Price"], log_x=True, title="Rating vs Reviews by Category",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig1.write_html("Day075/01_scatter.html")
print("Saved: 01_scatter.html")

fig2 = px.bar(
    df.groupby("Category").size().reset_index(name="Count").sort_values("Count"),
    x="Count", y="Category", orientation="h", title="Apps per Category",
    color="Count", color_continuous_scale="Blues"
)
fig2.write_html("Day075/02_bars.html")
print("Saved: 02_bars.html")

fig3 = px.box(
    df, x="Category", y="Rating", color="Category", title="Rating Distribution by Category",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig3.write_html("Day075/03_boxplot.html")
print("Saved: 03_boxplot.html")

fig4 = px.pie(
    df, names="Free", title="Free vs Paid Apps",
    color_discrete_sequence=["#2ecc71", "#e74c3c"],
    hole=0.4
)
fig4.write_html("Day075/04_pie.html")
print("Saved: 04_pie.html")

fig5 = px.sunburst(
    df, path=["Free", "Category"], values="Reviews",
    title="Review Distribution: Free/Paid → Category",
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig5.write_html("Day075/05_sunburst.html")
print("Saved: 05_sunburst.html")

df.to_csv("Day075/app_store_data.csv", index=False)
print("\nData saved to Day075/app_store_data.csv")
print("\nOpen any .html file in a browser to view interactive charts.")
