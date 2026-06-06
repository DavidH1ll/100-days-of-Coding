import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
np.random.seed(42)

print("=" * 60)
print("DAY 100 CAPSTONE: PREDICTING EARNINGS")
print("Multivariable Regression Analysis")
print("=" * 60)

# Generate synthetic earnings data
n = 5000
data = {
    "education_years": np.random.randint(8, 22, n),
    "experience_years": np.random.randint(0, 40, n),
    "hours_per_week": np.random.randint(20, 80, n),
    "age": np.random.randint(18, 65, n),
    "certifications": np.random.poisson(2, n),
    "job_category": np.random.choice(["Tech", "Finance", "Healthcare", "Education", "Retail", "Manufacturing"], n),
}

df = pd.DataFrame(data)
job_multipliers = {"Tech": 1.5, "Finance": 1.4, "Healthcare": 1.2, "Education": 0.9, "Retail": 0.7, "Manufacturing": 0.85}
df["base_earnings"] = (
    15000 +
    df["education_years"] * 2500 +
    df["experience_years"] * 1200 +
    df["hours_per_week"] * 200 +
    df["certifications"] * 3000 +
    np.random.normal(0, 10000, n)
)
df["earnings"] = df["base_earnings"] * df["job_category"].map(job_multipliers)
df["earnings"] = np.clip(df["earnings"], 15000, 250000).astype(int)
df = df.drop("base_earnings", axis=1)

df = pd.get_dummies(df, columns=["job_category"], drop_first=True)

print(f"\nDataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Earnings range: ${df['earnings'].min():,.0f} - ${df['earnings'].max():,.0f}")
print(f"Mean earnings: ${df['earnings'].mean():,.0f}")

# EDA
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Earnings Prediction: Exploratory Data Analysis", fontsize=14, fontweight="bold")

features = ["education_years", "experience_years", "hours_per_week", "age", "certifications", "earnings"]
for i, feat in enumerate(features):
    ax = axes[i // 3, i % 3]
    if feat == "earnings":
        ax.hist(df[feat], bins=40, color="#2ecc71", edgecolor="white")
        ax.set_title("Target: Earnings Distribution")
    else:
        ax.scatter(df[feat], df["earnings"], alpha=0.3, s=5, color="#3498db")
        ax.set_title(f"Earnings vs {feat.replace('_', ' ').title()}")
    ax.set_xlabel(feat.replace("_", " ").title())
    if i % 3 == 0:
        ax.set_ylabel("Earnings ($)")

plt.tight_layout()
plt.savefig("Day100/eda_dashboard.png", dpi=150)
print("Saved: eda_dashboard.png")
plt.close()

# Correlation heatmap
fig, ax = plt.subplots(figsize=(12, 10))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, cmap="coolwarm", center=0, fmt=".2f",
            square=True, ax=ax)
ax.set_title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig("Day100/correlation_heatmap.png", dpi=150)
print("Saved: correlation_heatmap.png")
plt.close()

# Model preparation
X = df.drop("earnings", axis=1)
y = df["earnings"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train multiple models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
}

results = []
print("\n--- Model Performance ---")
print(f"{'Model':<22} {'MAE':>10} {'RMSE':>10} {'R²':>8} {'CV R²':>8}")
print("-" * 60)

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)

    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="r2")
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()

    results.append({"Model": name, "MAE": mae, "RMSE": rmse, "R²": r2, "CV_R²": cv_mean, "CV_Std": cv_std})
    print(f"{name:<22} ${mae:>8,.0f} ${rmse:>8,.0f} {r2:>7.4f} {cv_mean:>7.4f} (±{cv_std:.4f})")

# Best model: Gradient Boosting
best_model = models["Gradient Boosting"]

# Grid Search on best model
print("\n--- Hyperparameter Tuning (Gradient Boosting) ---")
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.05, 0.1, 0.2],
}
grid = GridSearchCV(GradientBoostingRegressor(random_state=42), param_grid,
                     cv=3, scoring="r2", n_jobs=-1)
grid.fit(X_train_scaled, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best CV R²: {grid.best_score_:.4f}")

final_pred = grid.best_estimator_.predict(X_test_scaled)
final_r2 = r2_score(y_test, final_pred)
final_mae = mean_absolute_error(y_test, final_pred)
print(f"Tuned model R²: {final_r2:.4f}")
print(f"Tuned model MAE: ${final_mae:,.0f}")

# Feature importance
importance = grid.best_estimator_.feature_importances_
feature_names = X.columns

fig, ax = plt.subplots(figsize=(10, 6))
importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importance})
importance_df = importance_df.sort_values("Importance")
ax.barh(importance_df["Feature"], importance_df["Importance"], color="steelblue")
ax.set_title("Feature Importance (Tuned Gradient Boosting)")
ax.set_xlabel("Importance")
plt.tight_layout()
plt.savefig("Day100/feature_importance.png", dpi=150)
print("Saved: feature_importance.png")
plt.close()

# Predictions vs Actual
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(y_test, final_pred, alpha=0.3, s=8, color="#3498db")
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", linewidth=2)
ax.set_xlabel("Actual Earnings ($)")
ax.set_ylabel("Predicted Earnings ($)")
ax.set_title(f"Actual vs Predicted (R² = {final_r2:.4f})")
plt.tight_layout()
plt.savefig("Day100/predictions_vs_actual.png", dpi=150)
print("Saved: predictions_vs_actual.png")
plt.close()

# Save predictions
output = pd.DataFrame({"Actual": y_test.values, "Predicted": final_pred.round(0).astype(int),
                        "Error": (final_pred - y_test).round(0).astype(int)})
output.to_csv("Day100/predictions.csv", index=False)
print("Predictions saved to Day100/predictions.csv")

# Results summary
results_df = pd.DataFrame(results)
results_df.to_csv("Day100/model_comparison.csv", index=False)
print("Model comparison saved to Day100/model_comparison.csv")

print("\n" + "=" * 60)
print("DAY 100 COMPLETE!")
print(f"Best Model: Gradient Boosting (R² = {final_r2:.4f})")
print(f"Top 3 Features: {', '.join(importance_df.tail(3)['Feature'].values[::-1])}")
print("=" * 60)
