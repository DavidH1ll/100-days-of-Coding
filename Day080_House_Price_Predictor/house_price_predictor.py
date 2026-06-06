import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

print("=" * 60)
print("CAPSTONE: HOUSE PRICE PREDICTION")
print("=" * 60)

housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df["Price"] = housing.target

print(f"\nDataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Features: {housing.feature_names}")
print(f"\nTarget: Median House Value ($100,000s)")
print(f"Price range: ${df['Price'].min()*100000:,.0f} - ${df['Price'].max()*100000:,.0f}")

# EDA
print("\n--- Data Summary ---")
print(df.describe().round(2))

X = df.drop("Price", axis=1)
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Linear Regression
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
lr_pred = lr.predict(X_test_scaled)

lr_mae = mean_absolute_error(y_test, lr_pred)
lr_mse = mean_squared_error(y_test, lr_pred)
lr_rmse = np.sqrt(lr_mse)
lr_r2 = r2_score(y_test, lr_pred)

print("\n--- Linear Regression Results ---")
print(f"MAE:  ${lr_mae*100000:,.0f}")
print(f"RMSE: ${lr_rmse*100000:,.0f}")
print(f"R²:   {lr_r2:.4f}")

# Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
rf_pred = rf.predict(X_test_scaled)

rf_mae = mean_absolute_error(y_test, rf_pred)
rf_mse = mean_squared_error(y_test, rf_pred)
rf_rmse = np.sqrt(rf_mse)
rf_r2 = r2_score(y_test, rf_pred)

print("\n--- Random Forest Results ---")
print(f"MAE:  ${rf_mae*100000:,.0f}")
print(f"RMSE: ${rf_rmse*100000:,.0f}")
print(f"R²:   {rf_r2:.4f}")

# Cross-validation
lr_cv = cross_val_score(lr, X_train_scaled, y_train, cv=5, scoring="r2")
rf_cv = cross_val_score(rf, X_train_scaled, y_train, cv=5, scoring="r2")
print(f"\n--- 5-Fold Cross-Validation R² ---")
print(f"Linear Regression: {lr_cv.mean():.4f} (±{lr_cv.std():.4f})")
print(f"Random Forest:     {rf_cv.mean():.4f} (±{rf_cv.std():.4f})")

# Feature importance
print("\n--- Random Forest Feature Importance ---")
for name, imp in sorted(zip(housing.feature_names, rf.feature_importances_), key=lambda x: x[1], reverse=True):
    print(f"  {name}: {imp:.4f}")

# Sample predictions
print("\n--- Sample Predictions ---")
sample_indices = np.random.choice(len(y_test), 5, replace=False)
for i, idx in enumerate(sample_indices):
    actual = y_test.iloc[idx] * 100000
    predicted = rf_pred[idx] * 100000
    diff = predicted - actual
    print(f"  House {i+1}: Actual ${actual:,.0f} | Predicted ${predicted:,.0f} | Diff ${diff:+,.0f}")

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("House Price Prediction Analysis", fontsize=14, fontweight="bold")

axes[0, 0].scatter(y_test, lr_pred, alpha=0.4, s=10, label="Linear Regression")
axes[0, 0].scatter(y_test, rf_pred, alpha=0.4, s=10, label="Random Forest")
axes[0, 0].plot([0, 5], [0, 5], "r--", linewidth=1)
axes[0, 0].set_xlabel("Actual Price ($100k)")
axes[0, 0].set_ylabel("Predicted Price ($100k)")
axes[0, 0].set_title("Actual vs Predicted")
axes[0, 0].legend()

imp_df = pd.DataFrame({"Feature": housing.feature_names, "Importance": rf.feature_importances_})
imp_df = imp_df.sort_values("Importance")
axes[0, 1].barh(imp_df["Feature"], imp_df["Importance"], color="steelblue")
axes[0, 1].set_title("Feature Importance (Random Forest)")

corr = df.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=axes[1, 0], square=True)
axes[1, 0].set_title("Correlation Matrix")

models = ["Linear Regression", "Random Forest"]
mae_scores = [lr_mae * 100000, rf_mae * 100000]
rmse_scores = [lr_rmse * 100000, rf_rmse * 100000]
x = np.arange(len(models))
width = 0.35
axes[1, 1].bar(x - width/2, mae_scores, width, label="MAE", color="#3498db")
axes[1, 1].bar(x + width/2, rmse_scores, width, label="RMSE", color="#e74c3c")
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(models)
axes[1, 1].set_title("Model Error Comparison ($)")
axes[1, 1].set_ylabel("Error ($)")
axes[1, 1].legend()

plt.tight_layout()
plt.savefig("Day080/house_price_analysis.png", dpi=150, bbox_inches="tight")
print("\nChart saved to Day080/house_price_analysis.png")
plt.close()

results = pd.DataFrame({"Actual": y_test.values, "LR_Predicted": lr_pred, "RF_Predicted": rf_pred})
results.to_csv("Day080/predictions.csv", index=False)
print("Predictions saved to Day080/predictions.csv")
