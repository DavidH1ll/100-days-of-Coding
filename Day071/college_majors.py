import pandas as pd
import numpy as np

np.random.seed(42)

majors = [
    "Computer Science", "Electrical Engineering", "Mechanical Engineering",
    "Business Administration", "Economics", "Mathematics", "Physics",
    "Chemistry", "Biology", "English Literature", "History", "Psychology",
    "Political Science", "Nursing", "Education", "Communications",
    "Finance", "Marketing", "Architecture", "Philosophy"
]

categories = {
    "Computer Science": "STEM", "Electrical Engineering": "STEM",
    "Mechanical Engineering": "STEM", "Mathematics": "STEM",
    "Physics": "STEM", "Chemistry": "STEM", "Biology": "STEM",
    "Architecture": "STEM",
    "Business Administration": "Business", "Economics": "Business",
    "Finance": "Business", "Marketing": "Business",
    "English Literature": "Humanities", "History": "Humanities",
    "Philosophy": "Humanities", "Communications": "Humanities",
    "Political Science": "Social Sciences", "Psychology": "Social Sciences",
    "Nursing": "Health", "Education": "Education"
}

data = {
    "Major": majors,
    "Category": [categories[m] for m in majors],
    "Median_Salary": np.random.randint(35000, 130000, len(majors)),
    "P25_Salary": np.random.randint(25000, 90000, len(majors)),
    "P75_Salary": np.random.randint(50000, 180000, len(majors)),
    "Employment_Rate": np.round(np.random.uniform(0.65, 0.98, len(majors)), 3),
    "Total_Employed": np.random.randint(5000, 500000, len(majors)),
    "Unemployment_Rate": np.round(np.random.uniform(0.01, 0.12, len(majors)), 3),
}

df = pd.DataFrame(data)
df.loc[5, "Median_Salary"] = np.nan

print("=" * 60)
print("COLLEGE MAJOR SALARY ANALYSIS")
print("=" * 60)

print("\n--- First 5 rows ---")
print(df.head())

print("\n--- Last 5 rows ---")
print(df.tail())

print(f"\n--- Shape: {df.shape[0]} rows, {df.shape[1]} columns ---")

print("\n--- Column names ---")
print(df.columns.tolist())

print("\n--- Missing values ---")
print(df.isna().sum())

print("\n--- Summary statistics ---")
print(df.describe())

print("\n--- Majors by category ---")
print(df["Category"].value_counts())

print("\n--- Top 5 highest paying majors ---")
print(df.dropna(subset=["Median_Salary"])
      .sort_values("Median_Salary", ascending=False)[["Major", "Median_Salary", "Category"]]
      .head())

print("\n--- Lowest 5 paying majors ---")
print(df.dropna(subset=["Median_Salary"])
      .sort_values("Median_Salary")[["Major", "Median_Salary", "Category"]]
      .head())

print("\n--- Average salary by category ---")
category_stats = df.groupby("Category").agg(
    Avg_Salary=("Median_Salary", "mean"),
    Avg_Employment=("Employment_Rate", "mean"),
    Count=("Major", "count")
).sort_values("Avg_Salary", ascending=False)
print(category_stats.round(2))

print("\n--- STEM majors with salary > $80,000 ---")
stem_high = df[(df["Category"] == "STEM") & (df["Median_Salary"] > 80000)]
print(stem_high[["Major", "Median_Salary"]])

df.to_csv("Day071/college_majors.csv", index=False)
print("\nData saved to Day071/college_majors.csv")
