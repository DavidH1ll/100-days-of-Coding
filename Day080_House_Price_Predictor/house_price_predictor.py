"""Day 80 capstone: predict California house prices with Linear Regression and Random Forest.

Compares two regression models on the California Housing dataset with
cross-validation, feature importance, and a 4-panel diagnostic chart.
Outputs go to ``figures/`` (PNGs) and ``data/`` (CSVs); both are
gitignored.

Run from the command line:

    python house_price_predictor.py

Or import the pipeline:

    from house_price_predictor import run_pipeline
    run_pipeline()
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
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

OUTPUT_DIR = Path(__file__).parent
FIGURES_DIR = OUTPUT_DIR / "figures"
DATA_DIR = OUTPUT_DIR / "data"

RANDOM_STATE = 42
TEST_SIZE = 0.2
RF_N_ESTIMATORS = 100
CV_FOLDS = 5

TARGET_COL = "Price"
TARGET_DOLLAR_MULTIPLIER = 100_000  # CA housing target is in $100,000 units


def load_housing_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load the California Housing dataset as a DataFrame + target Series.

    Returns:
        Tuple of (features_with_target_df, target_series).
    """
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df[TARGET_COL] = housing.target
    return df, df[TARGET_COL]


def summarise_data(df: pd.DataFrame) -> None:
    """Print a rounded describe() of the data to stdout."""
    print("\n--- Data Summary ---")
    print(df.describe().round(2))


def split_data(
    df: pd.DataFrame,
    target_col: str = TARGET_COL,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple[np.ndarray, np.ndarray, pd.Series, pd.Series, StandardScaler]:
    """Split into scaled train/test sets, returning the fitted scaler too."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
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


def compute_metrics(
    y_true: pd.Series,
    y_pred: np.ndarray,
) -> dict[str, float]:
    """Return MAE, RMSE, and R^2 in real-dollar units."""
    mae = mean_absolute_error(y_true, y_pred) * TARGET_DOLLAR_MULTIPLIER
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred))) * TARGET_DOLLAR_MULTIPLIER
    r2 = r2_score(y_true, y_pred)
    return {"mae": mae, "rmse": rmse, "r2": r2}


def train_linear_regression(
    X_train: np.ndarray,
    y_train: pd.Series,
    X_test: np.ndarray,
    y_test: pd.Series,
) -> tuple[LinearRegression, dict[str, float]]:
    """Fit a Linear Regression model and return (model, metrics)."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return model, compute_metrics(y_test, pred)


def train_random_forest(
    X_train: np.ndarray,
    y_train: pd.Series,
    X_test: np.ndarray,
    y_test: pd.Series,
    n_estimators: int = RF_N_ESTIMATORS,
) -> tuple[RandomForestRegressor, dict[str, float]]:
    """Fit a Random Forest Regressor and return (model, metrics)."""
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return model, compute_metrics(y_test, pred)


def cross_validate_model(
    model: Any,
    X_train: np.ndarray,
    y_train: pd.Series,
    cv: int = CV_FOLDS,
) -> tuple[float, float]:
    """Return (mean, std) of 5-fold CV R^2."""
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="r2")
    return float(scores.mean()), float(scores.std())


def print_metrics(name: str, metrics: dict[str, float]) -> None:
    """Print metrics in a standard format."""
    print(f"\n--- {name} Results ---")
    print(f"MAE:  ${metrics['mae']:,.0f}")
    print(f"RMSE: ${metrics['rmse']:,.0f}")
    print(f"R2:   {metrics['r2']:.4f}")


def print_cv_comparison(cv_results: dict[str, tuple[float, float]]) -> None:
    """Print 5-fold CV R^2 for each model."""
    print(f"\n--- {CV_FOLDS}-Fold Cross-Validation R2 ---")
    for name, (mean, std) in cv_results.items():
        print(f"{name}: {mean:.4f} (+/-{std:.4f})")


def print_feature_importance(
    feature_names: list[str],
    importances: np.ndarray,
) -> None:
    """Print feature importances sorted high to low."""
    print("\n--- Random Forest Feature Importance ---")
    pairs = sorted(
        zip(feature_names, importances, strict=False),
        key=lambda x: x[1],
        reverse=True,
    )
    for name, imp in pairs:
        print(f"  {name}: {imp:.4f}")


def plot_feature_importance(
    feature_names: list[str],
    importances: np.ndarray,
    output_path: Path,
) -> None:
    """Save a horizontal bar chart of feature importances to ``output_path``."""
    imp_df = pd.DataFrame(
        {"Feature": feature_names, "Importance": importances},
    ).sort_values("Importance")
    _fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(imp_df["Feature"], imp_df["Importance"], color="steelblue")
    ax.set_title("Feature Importance (Random Forest)")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_predictions_vs_actual(
    y_test: pd.Series,
    predictions: dict[str, np.ndarray],
    output_path: Path,
) -> None:
    """Save a scatter of predicted vs actual for each model."""
    _fig, ax = plt.subplots(figsize=(8, 8))
    for name, pred in predictions.items():
        ax.scatter(y_test, pred, alpha=0.4, s=10, label=name)
    lo, hi = 0, 5
    ax.plot([lo, hi], [lo, hi], "r--", linewidth=1)
    ax.set_xlabel("Actual Price ($100k)")
    ax.set_ylabel("Predicted Price ($100k)")
    ax.set_title("Actual vs Predicted")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_model_comparison(
    metrics: dict[str, dict[str, float]],
    output_path: Path,
) -> None:
    """Save a side-by-side MAE/RMSE bar chart for each model."""
    names = list(metrics.keys())
    mae_scores = [metrics[n]["mae"] for n in names]
    rmse_scores = [metrics[n]["rmse"] for n in names]
    x = np.arange(len(names))
    width = 0.35
    _fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x - width / 2, mae_scores, width, label="MAE", color="#3498db")
    ax.bar(x + width / 2, rmse_scores, width, label="RMSE", color="#e74c3c")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_title("Model Error Comparison ($)")
    ax.set_ylabel("Error ($)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_correlation_matrix(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save a heatmap of pairwise feature correlations."""
    corr = df.corr()
    _fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".2f",
        ax=ax,
        square=True,
    )
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def save_predictions(
    y_test: pd.Series,
    predictions: dict[str, np.ndarray],
    output_path: Path,
) -> pd.DataFrame:
    """Save actual + per-model predicted values to a CSV and return it."""
    output = pd.DataFrame({"Actual": y_test.values})
    for name, pred in predictions.items():
        output[f"{name}_Predicted"] = pred
    output.to_csv(output_path, index=False)
    return output


def run_pipeline(figures_dir: Path | None = None, data_dir: Path | None = None) -> dict[str, Any]:
    """Run the full California house-price pipeline end to end.

    Loads the bundled sklearn dataset, trains both models, evaluates
    them, writes figures to ``figures_dir/`` and predictions to
    ``data_dir/predictions.csv``.

    Args:
        figures_dir: Where to write PNGs. Defaults to ``./figures``.
        data_dir: Where to write CSVs. Defaults to ``./data``.

    Returns:
        Dict with the trained models, their metrics, the CV results,
        and the test predictions.
    """
    if figures_dir is None:
        figures_dir = FIGURES_DIR
    if data_dir is None:
        data_dir = DATA_DIR
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("CAPSTONE: HOUSE PRICE PREDICTION")
    print("=" * 60)

    df, _ = load_housing_data()
    print(f"\nDataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Target: Median House Value (${TARGET_DOLLAR_MULTIPLIER:,}s)")
    print(
        f"Price range: ${df[TARGET_COL].min() * TARGET_DOLLAR_MULTIPLIER:,.0f} - "
        f"${df[TARGET_COL].max() * TARGET_DOLLAR_MULTIPLIER:,.0f}",
    )
    summarise_data(df)

    plot_correlation_matrix(df, figures_dir / "correlation_matrix.png")
    print("\nSaved: figures/correlation_matrix.png")

    X_train, X_test, y_train, y_test, _ = split_data(df)

    lr_model, lr_metrics = train_linear_regression(X_train, y_train, X_test, y_test)
    print_metrics("Linear Regression", lr_metrics)

    rf_model, rf_metrics = train_random_forest(X_train, y_train, X_test, y_test)
    print_metrics("Random Forest", rf_metrics)

    cv_results = {
        "Linear Regression": cross_validate_model(lr_model, X_train, y_train),
        "Random Forest": cross_validate_model(rf_model, X_train, y_train),
    }
    print_cv_comparison(cv_results)

    print_feature_importance(
        list(df.drop(columns=[TARGET_COL]).columns),
        rf_model.feature_importances_,
    )

    feature_names = list(df.drop(columns=[TARGET_COL]).columns)
    plot_feature_importance(
        feature_names,
        rf_model.feature_importances_,
        figures_dir / "feature_distributions.png",
    )
    print("Saved: figures/feature_distributions.png")

    predictions = {
        "Linear Regression": lr_model.predict(X_test),
        "Random Forest": rf_model.predict(X_test),
    }
    plot_predictions_vs_actual(
        y_test,
        predictions,
        figures_dir / "model_evaluation.png",
    )
    print("Saved: figures/model_evaluation.png")

    metrics = {"Linear Regression": lr_metrics, "Random Forest": rf_metrics}
    plot_model_comparison(metrics, figures_dir / "model_comparison.png")
    print("Saved: figures/model_comparison.png")

    save_predictions(y_test, predictions, data_dir / "predictions.csv")
    print("Predictions saved to data/predictions.csv")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    return {
        "models": {"Linear Regression": lr_model, "Random Forest": rf_model},
        "metrics": metrics,
        "cv_results": cv_results,
        "predictions": predictions,
    }


if __name__ == "__main__":
    run_pipeline()
