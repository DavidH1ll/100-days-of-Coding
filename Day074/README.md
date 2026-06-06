# Day 74 - Google Trends: Resampling & Time Series

## Overview
Synthetic search trend data over 2 years visualized with resampling (daily→weekly→monthly→quarterly), rolling averages, and seasonality detection by day of year.

## Key Concepts
- pd.date_range(), DatetimeIndex, .resample(), .rolling()
- Time series plotting, seasonality analysis
- .groupby() by day-of-year

## Reflection
`.resample()` is the Swiss Army knife of time series — one method handles all granularity changes. The 30-day rolling average smoothed out noise while preserving trends. Plotting by day-of-year revealed subtle seasonal patterns invisible in the raw data.

**Day 74 Complete!** ✅
