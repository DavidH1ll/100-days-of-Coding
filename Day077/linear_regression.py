import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

sns.set_theme(style="whitegrid")
mpg = sns.load_dataset("mpg").dropna()

print("=" * 60)
print("LINEAR REGRESSION WITH SEABORN")
print("=" * 60)

print(f"\nDataset: {mpg.shape[0]} rows, {mpg.shape[1]} columns")
print(f"Columns: {mpg.columns.tolist()}")

# EDA
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("MPG Dataset: Linear Regression Analysis", fontsize=14, fontweight="bold")

sns.scatterplot(data=mpg, x="weight", y="mpg", hue="origin", ax=axes[0, 0], alpha=0.7)
axes[0, 0].set_title("MPG vs Weight by Origin")

numeric_cols = mpg.select_dtypes(include=[np.number]).columns
corr = mpg[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=axes[0, 1], square=True)
axes[0, 1].set_title("Correlation Matrix")

slope, intercept, r_value, p_value, std_err = stats.linregress(mpg["weight"], mpg["mpg"])
print(f"\n--- Weight vs MPG Regression ---")
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.2f}")
print(f"R-squared: {r_value**2:.4f}")
print(f"P-value: {p_value:.2e}")
print(f"Standard Error: {std_err:.4f}")

sns.regplot(data=mpg, x="weight", y="mpg", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=axes[1, 0])
axes[1, 0].set_title(f"Regression Line (R² = {r_value**2:.3f})")

predicted = slope * mpg["weight"] + intercept
residuals = mpg["mpg"] - predicted

sns.residplot(x=predicted, y=residuals, lowess=True, ax=axes[1, 1],
              scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
axes[1, 1].axhline(0, color="gray", linestyle="--")
axes[1, 1].set_title("Residual Plot")
axes[1, 1].set_xlabel("Fitted Values")

plt.tight_layout()
plt.savefig("Day077/linear_regression.png", dpi=150, bbox_inches="tight")
print("\nSaved: Day077/linear_regression.png")
plt.close()

# Pairplot
g = sns.pairplot(mpg[["mpg", "weight", "horsepower", "displacement", "acceleration"]],
                 diag_kind="kde", plot_kws={"alpha": 0.5})
g.fig.suptitle("Pairwise Relationships", y=1.02, fontsize=14)
g.savefig("Day077/pairplot.png", dpi=150, bbox_inches="tight")
print("Saved: Day077/pairplot.png")
plt.close()

# Multiple regression demo
print("\n--- Multiple Regression (weight + horsepower → mpg) ---")
X = mpg[["weight", "horsepower"]].values
y = mpg["mpg"].values
X_with_intercept = np.column_stack([np.ones(len(X)), X])
coefficients = np.linalg.lstsq(X_with_intercept, y, rcond=None)[0]
predictions = X_with_intercept @ coefficients
ss_res = np.sum((y - predictions) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1 - ss_res / ss_tot
print(f"Intercept: {coefficients[0]:.2f}")
print(f"Weight coefficient: {coefficients[1]:.4f}")
print(f"Horsepower coefficient: {coefficients[2]:.4f}")
print(f"Multiple R²: {r2:.4f}")
