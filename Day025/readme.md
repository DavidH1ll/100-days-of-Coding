# Day 25 – CSV Data Analysis (Pandas Intro)

## Overview
Practice reading, filtering, aggregating, and exporting tabular data using CSV files and pandas.

## Files
- weather_data.csv – sample daily weather dataset.
- 2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv – NYC squirrel census dataset.
- main.py – basic weather data manipulations (manual parsing / pandas).
- main_exercise.py – additional pandas operations.
- squirrel_census.py – counts squirrels by primary fur color; writes squirrel_count.csv.
- squirrel_count.csv – generated output summary.

## Key Concepts
- Reading CSV (manual vs pandas).
- DataFrame selection and column access.
- Converting rows/columns to lists.
- Aggregation (mean, max).
- Boolean filtering.
- Grouping and counting.
- Exporting DataFrame to CSV.

## How to Run
```bash
python main.py
python squirrel_census.py
```

## Example (Counting Fur Colors)
```python
import pandas as pd
df = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
counts = df["Primary Fur Color"].value_counts().rename_axis("Fur Color").reset_index(name="Count")
counts.to_csv("squirrel_count.csv", index=False)
```

## Enhancement Ideas
- Add CLI flags (input, output paths).
- Handle missing values explicitly.
- Plot distributions (matplotlib/seaborn).
- Convert outputs to JSON.
- Wrap logic into reusable functions.

## Next
Advance to state/geo data handling (Day 25 Part 2). 