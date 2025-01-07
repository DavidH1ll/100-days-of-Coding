import os
import pandas

 # Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# # Create the full path to the CSV file
csv_path = os.path.join(script_dir, "weather_data.csv")

# with open(csv_path) as data_file:
#     data = csv.reader(data_file)
#     weather_data = []
#     next(data)  # Skip the header row
#     for row in data:
#         weather_data.append(row)

# print(weather_data)

# temperatures = []
# for row in weather_data:
#     temperatures.append(int(row[1]))

# print(temperatures)

data = pandas.read_csv(csv_path)
temp_average = round(data["Temp"].mean(), 1)
temp_max = data["Temp"].max()
print(f"Average temperature: {temp_average}°C")
print(f"Max temperature: {temp_max}°C")

data[data["Day"] == "Monday"]
print(data[data["Day"] == "Monday"])

# Get the row with the highest temperature
hottest_day = data[data["Temp"] == data["Temp"].max()]
print("\nHottest day:")
print(hottest_day)