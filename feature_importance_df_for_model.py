import pandas as pd

# Read the CSV file
data = pd.read_csv('current_data.csv')

# Select the columns you want to keep
columns_to_keep = ['Longitude', 'Latitude', 'Presence', 'bio1', 'bio6', 'bio9', 'bio11', 'bio12', 'ngd10', 'gdd10']
filtered_data = data[columns_to_keep]

# Save the updated DataFrame to a new CSV file
filtered_data.to_csv('filtered_file.csv', index=False)
