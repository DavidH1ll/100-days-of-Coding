"""Day 100 capstone: predict earnings from education, experience, and other features.

This module generates a synthetic earnings dataset, performs exploratory
analysis, trains a small model zoo, tunes the best one with GridSearchCV,
and writes the trained model outputs to disk.

The data is synthetic — earnings are a deterministic function of the
features plus noise — so the metrics are illustrative rather than
predictive of any real-world outcome. The point of this project is the
pipeline structure, not the model accuracy.

Run from the command line:

    python earnings_predictor.py

Or import the pipeline:

    from earnings_predictor import run_pipeline
    run_pipeline(output_dir=Path("./out"))
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
np.random.seed(42)

OUTPUT_DIR = Path(__file__).parent
DATA_N = 5000
TEST_SIZE = 0.2
RANDOM_STATE = 42

JOB_CATEGORIES = [
    "Tech",
    "Finance",
    "Healthcare",
    "Education",
    "Retail",
    "Manufacturing",
]
JOB_MULTIPLIERS = {
    "Tech": 1.5,
    "Finance": 1.4,
    "Healthcare": 1.2,
    "Education": 0.9,
    "Retail": 0.7,
    "Manufacturing": 0.85,
}

NUMERIC_FEATURES = [
    "education_years",
    "experience_years",
    "hours_per_week",
    "age",
    "certifications",
    "earnings",
]
TARGET_COL = "earnings"

BASELINE_MODELS: dict[str, Any] = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=100,
        random_state=RANDOM_STATE,
    ),
}

GRADIENT_BOOSTING_PARAM_GRID: dict[str, list[Any]] = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.05, 0.1, 0.2],
}


def generate_synthetic_data(n: int = DATA_N, seed: int = RANDOM_STATE) -> pd.DataFrame:
    """Generate a synthetic earnings dataset for demonstration.

    Earnings are a deterministic function of the features plus noise.
    Relationships are chosen to be plausible (more education, experience,
    hours, and certs tend to increase pay; category multipliers reflect
    typical industry pay bands).

    For real use cases, replace this with a real dataset.

    Args:
        n: Number of rows to generate.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with numeric features and one-hot encoded job category.
    """
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "education_years": rng.integers(8, 22, n),
            "experience_years": rng.integers(0, 40, n),
            "hours_per_week": rng.integers(20, 80, n),
            "age": rng.integers(18, 65, n),
            "certifications": rng.poisson(2, n),
            "job_category": rng.choice(JOB_CATEGORIES, n),
        },
    )

    base_earnings = (
        15000
        + df["education_years"] * 2500
        + df["experience_years"] * 1200
        + df["hours_per_week"] * 200
        + df["certifications"] * 3000
        + rng.normal(0, 10000, n)
    )
    df[TARGET_COL] = np.clip(
        base_earnings * df["job_category"].map(JOB_MULTIPLIERS),
        15_000,
        250_000,
    ).astype(int)

    return pd.get_dummies(df, columns=["job_category"], drop_first=True)


def plot_eda(df: pd.DataFrame, output_path: Path) -> None:
    """Save a 2x3 EDA grid to ``output_path``."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(
        "Earnings Prediction: Exploratory Data Analysis",
        fontsize=14,
        fontweight="bold",
    )

    for i, feat in enumerate(NUMERIC_FEATURES):
        ax = axes[i // 3, i % 3]
        if feat == TARGET_COL:
            ax.hist(df[feat], bins=40, color="#2ecc71", edgecolor="white")
            ax.set_title("Target: Earnings Distribution")
        else:
            ax.scatter(
                df[feat],
                df[TARGET_COL],
                alpha=0.3,
                s=5,
                color="#3498db",
            )
            ax.set_title(f"Earnings vs {feat.replace('_', ' ').title()}")
        ax.set_xlabel(feat.replace("_", " ").title())
        if i % 3 == 0:
            ax.set_ylabel("Earnings ($)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_correlation_matrix(df: pd.DataFrame, output_path: Path) -> None:
    """Save a triangle correlation heatmap to ``output_path``."""
    _fig, ax = plt.subplots(figsize=(12, 10))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".2f",
        square=True,
        ax=ax,
    )
    ax.set_title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def split_data(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple[np.ndarray, np.ndarray, pd.Series, pd.Series, StandardScaler]:
    """Split into train/test sets and standard-scale the features.

    Returns:
        Tuple of (X_train_scaled, X_test_scaled, y_train, y_test, scaler).
    """
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def evaluate_baseline_models(
    X_train: np.ndarray,
    y_train: pd.Series,
    X_test: np.ndarray,
    y_test: pd.Series,
) -> pd.DataFrame:
    """Train each baseline model and return a metrics DataFrame.

    Each row is one model, with MAE, RMSE, R², and 5-fold CV R² (mean and std).
    """
    results: list[dict[str, Any]] = []
    for name, model in BASELINE_MODELS.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, pred)
        rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
        r2 = r2_score(y_test, pred)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")

        results.append(
            {
                "Model": name,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
                "CV_R2": cv_scores.mean(),
                "CV_Std": cv_scores.std(),
            },
        )
    return pd.DataFrame(results)


def tune_gradient_boosting(
    X_train: np.ndarray,
    y_train: pd.Series,
    param_grid: dict[str, list[Any]] | None = None,
    cv: int = 3,
) -> GridSearchCV:
    """Tune a GradientBoostingRegressor via GridSearchCV.

    Args:
        X_train: Scaled training features.
        y_train: Training target.
        param_grid: Optional override for the search space.
        cv: Number of cross-validation folds.

    Returns:
        A fitted GridSearchCV instance with ``best_estimator_``, ``best_params_``,
        and ``best_score_`` available.
    """
    if param_grid is None:
        param_grid = GRADIENT_BOOSTING_PARAM_GRID
    grid = GridSearchCV(
        GradientBoostingRegressor(random_state=RANDOM_STATE),
        param_grid,
        cv=cv,
        scoring="r2",
        n_jobs=-1,
    )
    grid.fit(X_train, y_train)
    return grid


def plot_feature_importance(
    model: Any,
    feature_names: pd.Index,
    output_path: Path,
) -> pd.DataFrame:
    """Save a horizontal bar chart of feature importances.

    Returns the importance DataFrame (sorted ascending so the chart
    reads top-to-bottom from least to most important).
    """
    importance = model.feature_importances_
    importance_df = pd.DataFrame(
        {"Feature": feature_names, "Importance": importance},
    ).sort_values("Importance")

    _fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(importance_df["Feature"], importance_df["Importance"], color="steelblue")
    ax.set_title("Feature Importance (Tuned Gradient Boosting)")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return importance_df


def plot_predictions_vs_actual(
    y_test: pd.Series,
    predictions: np.ndarray,
    output_path: Path,
) -> None:
    """Save a scatter plot of predictions vs actual values."""
    _fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_test, predictions, alpha=0.3, s=8, color="#3498db")
    ax.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        "r--",
        linewidth=2,
    )
    ax.set_xlabel("Actual Earnings ($)")
    ax.set_ylabel("Predicted Earnings ($)")
    r2 = r2_score(y_test, predictions)
    ax.set_title(f"Actual vs Predicted (R² = {r2:.4f})")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_predictions(
    y_test: pd.Series,
    predictions: np.ndarray,
    output_path: Path,
) -> pd.DataFrame:
    """Write actual / predicted / error to a CSV and return the DataFrame."""
    output = pd.DataFrame(
        {
            "Actual": y_test.values,
            "Predicted": predictions.round(0).astype(int),
            "Error": (predictions - y_test).round(0).astype(int),
        },
    )
    output.to_csv(output_path, index=False)
    return output


def run_pipeline(output_dir: Path | None = None) -> dict[str, Any]:
    """Run the full earnings-prediction pipeline end to end.

    Generates synthetic data, performs EDA, trains and evaluates the
    baseline model zoo, tunes the best one with GridSearchCV, writes
    outputs to ``output_dir``, and returns a summary dict.

    Args:
        output_dir: Where to write PNGs and CSVs. Defaults to the
            module's parent directory.

    Returns:
        Dict with keys ``best_model``, ``best_params``, ``r2``,
        ``mae``, ``feature_importance``.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("DAY 100 CAPSTONE: PREDICTING EARNINGS")
    print("Multivariable Regression Analysis")
    print("=" * 60)

    df = generate_synthetic_data()
    print(
        f"\nDataset: {df.shape[0]} rows, {df.shape[1]} columns\n"
        f"Earnings range: ${df[TARGET_COL].min():,.0f} - ${df[TARGET_COL].max():,.0f}\n"
        f"Mean earnings: ${df[TARGET_COL].mean():,.0f}",
    )

    plot_eda(df, output_dir / "eda_dashboard.png")
    print("Saved: eda_dashboard.png")
    plot_correlation_matrix(df, output_dir / "correlation_heatmap.png")
    print("Saved: correlation_heatmap.png")

    X_train, X_test, y_train, y_test, _ = split_data(df)

    print("\n--- Model Performance ---")
    print(f"{'Model':<22} {'MAE':>10} {'RMSE':>10} {'R²':>8} {'CV R²':>8}")
    print("-" * 60)
    results = evaluate_baseline_models(X_train, y_train, X_test, y_test)
    for row in results.itertuples():
        print(
            f"{row.Model:<22} ${row.MAE:>8,.0f} ${row.RMSE:>8,.0f} "
            f"R²={row.R2:>7.4f} CV_R²={row.CV_R2:>7.4f} (±{row.CV_Std:.4f})",
        )
    results.to_csv(output_dir / "model_comparison.csv", index=False)
    print("Model comparison saved to model_comparison.csv")

    print("\n--- Hyperparameter Tuning (Gradient Boosting) ---")
    grid = tune_gradient_boosting(X_train, y_train)
    print(f"Best params: {grid.best_params_}")
    print(f"Best CV R²: {grid.best_score_:.4f}")

    final_pred = grid.best_estimator_.predict(X_test)
    final_r2 = r2_score(y_test, final_pred)
    final_mae = mean_absolute_error(y_test, final_pred)
    print(f"Tuned model R²: {final_r2:.4f}")
    print(f"Tuned model MAE: ${final_mae:,.0f}")

    feature_names = df.drop(columns=[TARGET_COL]).columns
    importance_df = plot_feature_importance(
        grid.best_estimator_,
        feature_names,
        output_dir / "feature_importance.png",
    )
    print("Saved: feature_importance.png")

    plot_predictions_vs_actual(
        y_test,
        final_pred,
        output_dir / "predictions_vs_actual.png",
    )
    print("Saved: predictions_vs_actual.png")

    save_predictions(y_test, final_pred, output_dir / "predictions.csv")
    print("Predictions saved to predictions.csv")

    print("\n" + "=" * 60)
    print("DAY 100 COMPLETE!")
    print(f"Best Model: Gradient Boosting (R² = {final_r2:.4f})")
    print(
        f"Top 3 Features: {', '.join(importance_df.tail(3)['Feature'].values[::-1])}",
    )
    print("=" * 60)

    return {
        "best_model": grid.best_estimator_,
        "best_params": grid.best_params_,
        "r2": final_r2,
        "mae": final_mae,
        "feature_importance": importance_df,
    }


if __name__ == "__main__":
    run_pipeline()
