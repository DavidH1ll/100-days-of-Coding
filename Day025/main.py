import os
import pandas as pd

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "weather_data.csv")

# Read the CSV file
data = pd.read_csv(csv_path)

# --- Basic inspection ---
print("Columns:", list(data.columns))
print("\nFirst few rows:")
print(data.head())

# --- Temperature analysis ---
temperatures = list(data["Temp"])
print(f"\nTemperatures: {temperatures}")
print(f"Average temperature: {round(sum(temperatures) / len(temperatures), 1)}°C")
print(f"Max temperature: {max(temperatures)}°C")

# --- Filter with pandas ---
monday_data = data[data["Day"] == "Monday"]
print("\nMonday weather:")
print(monday_data)

# --- Find hottest day ---
hottest_day = data[data["Temp"] == data["Temp"].max()]
print("\nHottest day:")
print(hottest_day)
