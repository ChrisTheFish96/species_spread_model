# import dependencies
import pandas as pd

# Read in absence and presence csv file with environmental variables
absence_csv = pd.read_csv('CLEANED_absence_data.csv', usecols=['Latitude', 'Longitude', 'Presence'])
presence_csv = pd.read_csv('data_files/CLEANED_S_frugiperda_data.csv', usecols=['decimalLongitude', 'decimalLatitude'])

# Add a new 'presence' column to csv2 and fill it with 1s
# Rename columns to match with that in the absence file
presence_csv['Presence'] = 1
presence_csv.rename(columns={'decimalLongitude': 'Longitude', 'decimalLatitude': 'Latitude'}, inplace=True)

# Concatenate the two DataFrames vertically
# Add a new column 'species' with a constant value
# Save the merged DataFrame to a new CSV file
merged_df = pd.concat([absence_csv, presence_csv], ignore_index=True)
merged_df.to_csv('train_test_pa_data.csv', index=False)

# Shuffle the rows of the merged DataFrame
shuffled_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)
# Save the shuffled DataFrame to a new CSV file
shuffled_df.to_csv('shuffled_train_test_pa_data.csv', index=False)