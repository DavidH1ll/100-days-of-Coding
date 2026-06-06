# Day 77 - Linear Regression & Seaborn

## Overview
Performed linear regression on the MPG dataset using scipy.stats and seaborn. Created regplots, residual plots, correlation heatmaps, and pairplots. Extended to multiple regression with weight + horsepower predicting MPG.

## Key Concepts
- scipy.stats.linregress() for single-variable regression
- sns.regplot(), sns.lmplot(), sns.heatmap(), sns.pairplot()
- R² interpretation, residual analysis, multiple regression with np.linalg.lstsq

## Reflection
The R² of 0.69 for weight alone means weight explains ~69% of MPG variance — that's strong for a single variable. The residual plot showed a slight funnel shape, hinting at heteroscedasticity. Adding horsepower only bumped R² to ~0.72, suggesting diminishing returns from additional predictors.

**Day 77 Complete!** ✅
