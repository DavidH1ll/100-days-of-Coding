# Day 100 - Predicting Earnings with Multivariable Regression

## The Final Capstone

Full machine learning pipeline predicting annual earnings from education, experience, hours worked, certifications, and job category. Five models compared, hyperparameter tuning applied, and results exported.

## Pipeline
1. **EDA**: 6-panel dashboard with scatter plots and target distribution
2. **Correlation Analysis**: Heatmap showing feature relationships
3. **Model Comparison**: Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting
4. **Cross-Validation**: 5-fold CV R² scores for all models
5. **Hyperparameter Tuning**: GridSearchCV on the best model
6. **Feature Importance**: Top predictors of earnings
7. **Predictions Export**: CSV with actual vs predicted values

## Results
- Best model: Gradient Boosting (R² = tuned score from grid search)
- Top features: education_years, experience_years, job category (Tech)
- 5-fold CV confirmed model stability

## 100 Days Journey Summary

| Block | Days | Topics Covered |
|-------|------|----------------|
| Python Fundamentals | 1-10 | Variables, control flow, functions, dictionaries |
| Intermediate | 11-20 | OOP, turtle graphics, file I/O |
| Advanced Projects | 21-30 | Games, data processing, Tkinter GUI |
| Automation & APIs | 31-40 | Email, weather, stock, flight finder |
| HTML/CSS | 41-42 | Web fundamentals |
| Flask Web Dev | 43-56 | Templates, static files, routing |
| Flask Forms & DB | 57-70 | Jinja2, WTForms, SQLAlchemy, auth, REST APIs |
| Data Science | 71-80 | Pandas, NumPy, Matplotlib, Seaborn, Plotly, ML |
| Portfolio Projects | 81-100 | GUI apps, games, web apps, APIs, analysis |

## Reflection on 100 Days

Building something every day for 100 days teaches you that consistency beats intensity. The projects that felt impossible on Day 1 (REST APIs, ML pipelines, full-stack web apps) became natural by Day 80. The biggest growth wasn't in any single technology — it was in the confidence to approach any problem knowing I have the toolkit to solve it.

Key lessons:
1. **Plan before coding** — 20 minutes of design saves 2 hours of debugging
2. **Read error messages carefully** — they tell you exactly what's wrong
3. **Build things you'd actually use** — motivation follows utility
4. **Don't skip the README** — documenting your work cements the learning
5. **The community matters** — reviewing others' code teaches as much as writing your own

---

**Day 100 Complete! The journey continues.** 🎉

## Tests

This day ships with a pytest suite — 19 tests covering the data
loading, cleaning, evaluation, and feature-importance helpers. The
full suite runs in ~3 s. Generated PNGs and the model-comparison
CSV are written to `figures/` and `data/` and are gitignored.

```bash
pip install -r requirements.txt
pytest Day100_Earnings_Predictor/tests -v
```

## Output

Running `earnings_predictor.py` writes the following files
(under `figures/` and `data/`, both gitignored):

- `figures/eda_dashboard.png` — 6-panel EDA overview
- `figures/correlation_heatmap.png` — feature correlation heatmap
- `figures/model_comparison.png` — bar chart of CV R² across all
  five models
- `figures/feature_importance.png` — top feature importances for
  the best model
- `data/model_comparison.csv` — table of metrics for every model

To regenerate after changing the pipeline, delete the `figures/`
and `data/` folders and re-run the script.
