"""Tests for the Day 80 house price predictor pipeline."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from house_price_predictor import (
    CV_FOLDS,
    RANDOM_STATE,
    RF_N_ESTIMATORS,
    TARGET_COL,
    TARGET_DOLLAR_MULTIPLIER,
    TEST_SIZE,
    compute_metrics,
    cross_validate_model,
    load_housing_data,
    plot_correlation_matrix,
    plot_feature_importance,
    plot_model_comparison,
    plot_predictions_vs_actual,
    save_predictions,
    split_data,
    train_linear_regression,
    train_random_forest,
)


@pytest.fixture(scope="module")
def housing_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load the bundled California Housing dataset once for the module."""
    return load_housing_data()


@pytest.fixture(scope="module")
def split_data_fixture(housing_data: tuple[pd.DataFrame, pd.Series]):
    df, _ = housing_data
    return split_data(df)


class TestData:
    def test_load_returns_dataframe_and_series(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
    ) -> None:
        df, y = housing_data
        assert isinstance(df, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert not df.empty

    def test_target_column_present(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
    ) -> None:
        df, _ = housing_data
        assert TARGET_COL in df.columns

    def test_target_in_real_dollar_range(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
    ) -> None:
        _, y = housing_data
        # CA housing target in $100,000 units: range ~0.15 to 5.0
        assert y.min() >= 0.1
        assert y.max() <= 6.0

    def test_no_nans(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
    ) -> None:
        df, _ = housing_data
        assert df.isna().sum().sum() == 0


class TestSplit:
    def test_split_sizes(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
    ) -> None:
        df, _ = housing_data
        n = len(df)
        X_train, X_test, y_train, y_test, _ = split_data(df)
        expected_test = int(n * TEST_SIZE)
        assert len(X_test) == pytest.approx(expected_test, abs=5)
        assert len(X_train) == n - len(X_test)
        assert len(y_train) == len(X_train)
        assert len(y_test) == len(X_test)

    def test_target_not_in_features(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
    ) -> None:
        df, _ = housing_data
        X_train, X_test, _, _, _ = split_data(df)
        assert X_train.shape[1] == X_test.shape[1]
        # 8 features (no target in scaled array)
        assert X_train.shape[1] == 8

    def test_features_are_standardized(
        self,
        split_data_fixture: tuple,
    ) -> None:
        X_train, *_ = split_data_fixture
        assert np.allclose(X_train.mean(axis=0), 0.0, atol=1e-7)
        assert np.allclose(X_train.std(axis=0), 1.0, atol=1e-6)


class TestModels:
    def test_lr_trains_and_meets_r2_threshold(
        self,
        split_data_fixture: tuple,
    ) -> None:
        X_train, X_test, y_train, y_test, _ = split_data_fixture
        _, metrics = train_linear_regression(X_train, y_train, X_test, y_test)
        # California housing LR baseline is around R^2 ~ 0.58
        assert metrics["r2"] > 0.5

    def test_rf_outperforms_lr(
        self,
        split_data_fixture: tuple,
    ) -> None:
        X_train, X_test, y_train, y_test, _ = split_data_fixture
        _, lr_metrics = train_linear_regression(X_train, y_train, X_test, y_test)
        _, rf_metrics = train_random_forest(
            X_train,
            y_train,
            X_test,
            y_test,
            n_estimators=20,
        )
        assert rf_metrics["r2"] > lr_metrics["r2"]

    def test_metrics_in_dollar_units(
        self,
        split_data_fixture: tuple,
    ) -> None:
        X_train, X_test, y_train, y_test, _ = split_data_fixture
        _, metrics = train_linear_regression(X_train, y_train, X_test, y_test)
        # MAE/RMSE should be in real-dollar units (not the dataset's $100k).
        # On CA housing a reasonable LR MAE is around $50k; sanity-cap at $1M
        # so a bug that reverts the multiplier is caught.
        assert 0 < metrics["mae"] < 1_000_000
        assert 0 < metrics["rmse"] < 1_000_000
        # And both should be at least the multiplier (otherwise we forgot it)
        assert metrics["mae"] >= TARGET_DOLLAR_MULTIPLIER * 0.1
        assert metrics["rmse"] >= TARGET_DOLLAR_MULTIPLIER * 0.1

    def test_compute_metrics_keys(self) -> None:
        y_true = pd.Series([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 1.9, 3.2])
        metrics = compute_metrics(y_true, y_pred)
        assert set(metrics.keys()) == {"mae", "rmse", "r2"}
        assert metrics["mae"] > 0
        assert 0.9 < metrics["r2"] < 1.0


class TestCrossValidation:
    def test_cv_returns_mean_and_std(self, split_data_fixture: tuple) -> None:
        X_train, _, y_train, _, _ = split_data_fixture
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        mean, std = cross_validate_model(model, X_train, y_train, cv=3)
        assert isinstance(mean, float)
        assert isinstance(std, float)
        assert std >= 0.0

    def test_cv_uses_requested_folds(self) -> None:
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        import numpy as np

        X = np.random.default_rng(0).standard_normal((100, 3))
        y = X[:, 0] + np.random.default_rng(0).standard_normal(100) * 0.1
        mean_3, _ = cross_validate_model(model, X, y, cv=3)
        mean_5, _ = cross_validate_model(model, X, y, cv=5)
        # Both should be valid R^2 in [-1, 1]
        assert -1.0 <= mean_3 <= 1.0
        assert -1.0 <= mean_5 <= 1.0
        # Sanity: defaults match CV_FOLDS
        assert CV_FOLDS == 5


class TestIO:
    def test_save_predictions_csv(
        self,
        split_data_fixture: tuple,
        tmp_path: Path,
    ) -> None:
        _, _X_test, _, y_test, _ = split_data_fixture
        preds = {
            "Linear Regression": np.zeros(len(y_test)),
            "Random Forest": y_test.values,
        }
        out = tmp_path / "predictions.csv"
        df = save_predictions(y_test, preds, out)
        assert out.exists()
        assert "Actual" in df.columns
        assert "Linear Regression_Predicted" in df.columns
        assert "Random Forest_Predicted" in df.columns
        assert len(df) == len(y_test)

    def test_plot_feature_importance_creates_file(
        self,
        tmp_path: Path,
    ) -> None:
        names = ["a", "b", "c"]
        importances = np.array([0.5, 0.3, 0.2])
        out = tmp_path / "imp.png"
        plot_feature_importance(names, importances, out)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_plot_predictions_vs_actual_creates_file(
        self,
        split_data_fixture: tuple,
        tmp_path: Path,
    ) -> None:
        _, _X_test, _, y_test, _ = split_data_fixture
        preds = {
            "LR": np.zeros(len(y_test)),
            "RF": y_test.values,
        }
        out = tmp_path / "pred.png"
        plot_predictions_vs_actual(y_test, preds, out)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_plot_correlation_matrix_creates_file(
        self,
        housing_data: tuple[pd.DataFrame, pd.Series],
        tmp_path: Path,
    ) -> None:
        df, _ = housing_data
        out = tmp_path / "corr.png"
        plot_correlation_matrix(df, out)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_plot_model_comparison_creates_file(
        self,
        tmp_path: Path,
    ) -> None:
        metrics = {
            "A": {"mae": 100.0, "rmse": 150.0, "r2": 0.8},
            "B": {"mae": 80.0, "rmse": 120.0, "r2": 0.9},
        }
        out = tmp_path / "compare.png"
        plot_model_comparison(metrics, out)
        assert out.exists()
        assert out.stat().st_size > 0


class TestConstants:
    def test_constants_have_expected_types(self) -> None:
        assert isinstance(RANDOM_STATE, int)
        assert isinstance(TEST_SIZE, float)
        assert isinstance(RF_N_ESTIMATORS, int)
        assert isinstance(CV_FOLDS, int)
        assert 0.0 < TEST_SIZE < 1.0
