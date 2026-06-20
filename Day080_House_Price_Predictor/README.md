# Day 80 - Capstone: Predict House Prices

## Overview
Full machine learning pipeline on the California Housing dataset. Compared Linear Regression and Random Forest models with cross-validation, feature importance analysis, and sample predictions.

## Key Concepts
- sklearn.model_selection (train_test_split, cross_val_score, GridSearchCV)
- sklearn.preprocessing.StandardScaler
- sklearn.ensemble.RandomForestRegressor
- MAE, MSE, RMSE, R² evaluation metrics
- Feature importance ranking

## Reflection
Random Forest (R²=0.81) significantly outperformed Linear Regression (R²=0.60) on this dataset. The non-linear relationships in housing data (location effects, threshold effects) are better captured by tree-based models. Cross-validation confirmed the RF advantage wasn't just luck on the test split.

**Day 80 Complete!** ✅

## Tests

This day ships with a pytest suite — 19 tests covering the data
loading, cleaning, and evaluation helpers. The full suite runs in
~2.6 s. Generated PNGs and the processed dataset are written to
`figures/` and `data/` and are gitignored.

```bash
pip install -r requirements.txt
pytest Day080_House_Price_Predictor/tests -v
```

## Output

Running `house_price_predictor.py` writes the following files
(under `figures/` and `data/`, both gitignored):

- `figures/correlation_matrix.png` — feature correlation heatmap
- `figures/feature_distributions.png` — per-feature histograms
- `figures/model_comparison.png` — predicted vs actual scatter for
  the chosen best model
- `figures/model_evaluation.png` — residual plot
- `data/california_clean.csv` — the processed dataset

To regenerate after changing the model or data, delete the
`figures/` and `data/` folders and re-run the script.
