# Day 79 - Handwashing Discovery: t-Tests & Distributions

## Overview
Recreated Dr. Semmelweis' 1847 discovery that handwashing reduces maternal mortality. Used synthetic mortality data, independent t-tests, distribution visualizations, and rolling averages to tell a data-driven story.

## Key Concepts
- scipy.stats.ttest_ind() for independent t-tests
- p-value interpretation and statistical significance
- sns.histplot() with KDE, sns.boxplot()
- Rolling averages for time series smoothing

## Reflection
The t-test between Clinic 1 before and after handwashing yielded p << 0.001 — overwhelming evidence. Meanwhile Clinic 2 (no handwashing) showed no significant change. This is the power of a natural experiment: one clinic changed, one didn't, and the data tells the story.

**Day 79 Complete!** ✅
