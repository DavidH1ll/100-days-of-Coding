import pandas as pd
import os

 # Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# # Create the full path to the CSV file
csv_path = os.path.join(script_dir, "2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_path)

# Count fur colors 
fur_color_counts = data["Primary Fur Color"].value_counts()

# Convert the counts to a DataFrame
fur_color_df = pd.DataFrame(fur_color_counts)
fur_color_df.columns = ["Count"]
fur_color_df.index.name = "Fur Color"

# Export to CSV in the same directory
output_path = os.path.join(script_dir, "squirrel_count.csv")
fur_color_df.to_csv(output_path)

print("\nSquirrel Fur Color Counts:")
print(fur_color_counts)
