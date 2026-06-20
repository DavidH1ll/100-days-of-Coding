"""Tests for the Day 100 earnings predictor pipeline."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from earnings_predictor import (
    BASELINE_MODELS,
    DATA_N,
    JOB_CATEGORIES,
    TARGET_COL,
    evaluate_baseline_models,
    generate_synthetic_data,
    plot_feature_importance,
    plot_predictions_vs_actual,
    save_predictions,
    split_data,
    tune_gradient_boosting,
)


@pytest.fixture
def small_data() -> pd.DataFrame:
    """Generate a small dataset for fast tests."""
    return generate_synthetic_data(n=200, seed=42)


@pytest.fixture
def split_small(small_data: pd.DataFrame) -> tuple:
    return split_data(small_data, test_size=0.2, random_state=42)


class TestDataGeneration:
    def test_returns_dataframe(self, small_data: pd.DataFrame) -> None:
        assert isinstance(small_data, pd.DataFrame)
        assert not small_data.empty

    def test_shape_matches_n(self, small_data: pd.DataFrame) -> None:
        # 5 numeric feature columns + 1 target + 5 one-hot dummies
        # (drop_first=True drops the alphabetically-first category, "Education")
        expected_cols = 5 + 1 + (len(JOB_CATEGORIES) - 1)
        assert small_data.shape == (200, expected_cols)

    def test_no_nans(self, small_data: pd.DataFrame) -> None:
        assert small_data.isna().sum().sum() == 0

    def test_target_in_expected_range(self, small_data: pd.DataFrame) -> None:
        assert small_data[TARGET_COL].min() >= 15_000
        assert small_data[TARGET_COL].max() <= 250_000

    def test_target_is_integer(self, small_data: pd.DataFrame) -> None:
        assert pd.api.types.is_integer_dtype(small_data[TARGET_COL])

    def test_seed_makes_reproducible(self) -> None:
        df1 = generate_synthetic_data(n=100, seed=123)
        df2 = generate_synthetic_data(n=100, seed=123)
        pd.testing.assert_frame_equal(df1, df2)

    def test_one_hot_columns_present(self, small_data: pd.DataFrame) -> None:
        # drop_first=True drops the first category alphabetically: "Education"
        dropped = "Education"
        for cat in JOB_CATEGORIES:
            col = f"job_category_{cat}"
            if cat == dropped:
                assert col not in small_data.columns
            else:
                assert col in small_data.columns

    def test_default_n(self) -> None:
        df = generate_synthetic_data()
        assert len(df) == DATA_N


class TestSplit:
    def test_split_sizes(self, small_data: pd.DataFrame) -> None:
        X_train, X_test, y_train, y_test, _ = split_data(
            small_data,
            test_size=0.2,
            random_state=42,
        )
        assert X_train.shape[0] == 160
        assert X_test.shape[0] == 40
        assert len(y_train) == 160
        assert len(y_test) == 40

    def test_target_not_in_features(self, split_small: tuple) -> None:
        X_train, X_test, _, _, _ = split_small
        # 5 numeric features + 5 one-hot dummies (Education dropped) = 10
        assert X_train.shape[1] == X_test.shape[1]
        assert X_train.shape[1] == 5 + (len(JOB_CATEGORIES) - 1)

    def test_returns_fitted_scaler(self, small_data: pd.DataFrame) -> None:
        _, _, _, _, scaler = split_data(small_data)
        assert hasattr(scaler, "transform")
        assert hasattr(scaler, "mean_")
        assert len(scaler.mean_) > 0

    def test_scaler_standardizes(self, split_small: tuple) -> None:
        X_train, *_ = split_small
        # After StandardScaler, mean should be ~0 and std ~1
        assert np.allclose(X_train.mean(axis=0), 0.0, atol=1e-7)
        assert np.allclose(X_train.std(axis=0), 1.0, atol=1e-6)


class TestModels:
    def test_baseline_returns_dataframe(self, split_small: tuple) -> None:
        X_train, X_test, y_train, y_test, _ = split_small
        results = evaluate_baseline_models(X_train, y_train, X_test, y_test)
        assert isinstance(results, pd.DataFrame)
        assert "Model" in results.columns
        assert "R2" in results.columns
        assert len(results) == len(BASELINE_MODELS)

    def test_baseline_r2_in_range(self, split_small: tuple) -> None:
        X_train, X_test, y_train, y_test, _ = split_small
        results = evaluate_baseline_models(X_train, y_train, X_test, y_test)
        # R² should be a real number; on synthetic data the trees will overfit hard
        for r2 in results["R2"]:
            assert isinstance(r2, float)
            assert -1.0 <= r2 <= 1.0

    def test_tune_returns_fitted_grid(self, split_small: tuple) -> None:
        X_train, _, y_train, _, _ = split_small
        grid = tune_gradient_boosting(
            X_train,
            y_train,
            param_grid={
                "n_estimators": [50],
                "max_depth": [3],
                "learning_rate": [0.1],
            },
            cv=2,
        )
        assert hasattr(grid, "best_estimator_")
        assert hasattr(grid, "best_params_")
        assert hasattr(grid, "best_score_")
        assert isinstance(grid.best_score_, float)


class TestIO:
    def test_save_predictions_writes_csv(
        self,
        split_small: tuple,
        tmp_path: Path,
    ) -> None:
        _, _, _, y_test, _ = split_small
        output_path = tmp_path / "predictions.csv"
        result = save_predictions(y_test, np.zeros(len(y_test)), output_path)
        assert output_path.exists()
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["Actual", "Predicted", "Error"]
        assert len(result) == len(y_test)

    def test_save_predictions_error_column_accurate(
        self,
        split_small: tuple,
        tmp_path: Path,
    ) -> None:
        _, _, _, y_test, _ = split_small
        output_path = tmp_path / "predictions.csv"
        preds = y_test.values + 100  # off by 100 each
        result = save_predictions(y_test, preds, output_path)
        assert (result["Error"] == 100).all()

    def test_plot_predictions_creates_file(
        self,
        split_small: tuple,
        tmp_path: Path,
    ) -> None:
        _, _, _, y_test, _ = split_small
        output_path = tmp_path / "predictions.png"
        plot_predictions_vs_actual(y_test, y_test.values, output_path)
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_plot_feature_importance_creates_file(
        self,
        split_small: tuple,
        tmp_path: Path,
    ) -> None:
        X_train, _, y_train, _, _ = split_small
        grid = tune_gradient_boosting(
            X_train,
            y_train,
            param_grid={
                "n_estimators": [10],
                "max_depth": [3],
                "learning_rate": [0.1],
            },
            cv=2,
        )
        feature_names = pd.Index([f"f{i}" for i in range(X_train.shape[1])])
        output_path = tmp_path / "importance.png"
        importance_df = plot_feature_importance(
            grid.best_estimator_,
            feature_names,
            output_path,
        )
        assert output_path.exists()
        assert isinstance(importance_df, pd.DataFrame)
        assert "Feature" in importance_df.columns
        assert "Importance" in importance_df.columns
        # Importances should sum to ~1
        assert importance_df["Importance"].sum() == pytest.approx(1.0, abs=1e-6)
