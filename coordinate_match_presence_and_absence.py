# Import all the required packages
import pandas as pd
from scipy.spatial import distance

# Read the CSV files into Pandas DataFrames
presence_df = pd.read_csv("CLEANED_S_frugiperda_data_present.csv")
absence_df = pd.read_csv("CLEANED_S_frugiperda_data_absent.csv")

specific_columns_absent = ["Longitude", "Latitude"]
absence_df_coordinates = absence_df[specific_columns_absent]

specific_columns_present = ["decimalLongitude", "decimalLatitude"]
presence_df_coordinates = presence_df[specific_columns_present]

bio_df = pd.read_csv("combined_data.csv")
bio_df.columns = bio_df.columns.str.strip()

# For each row in the CLEANED_S_frugiperda_data_absent.csv find the closest matching coordinate in the combined_data.csv
# Add bio1-bio19 values of closest point to the absence_df
# Create a csv file with absence data and bio variables 
for index, row in absence_df_coordinates.iterrows():
    print(f"Finding {index}")
    absence_lat = row["Latitude"]
    absence_lon = row["Longitude"]
    
    # Calculate the distances between the occurrence point and all points in bio_df
    distances = bio_df.apply(
    lambda x: distance.euclidean((x["longitude"], x["latitude"]), (absence_lon, absence_lat)), axis=1
    )
    
    # Find the index of the row with the minimum distance
    closest_index = distances.idxmin()
    
    # Get the corresponding environmental variables from temps_df
    environmental_variables = bio_df.loc[closest_index, bio_df.columns[2:]]
    
    # Add the environmental variables to the occurrence row
    absence_df.loc[index, bio_df.columns[2:]] = environmental_variables
print("complete")
absence_df.to_csv("absence_with_bio.csv", index=False)

# Same as previous for loop only for CLEANED_S_frugiperda_data
for index, row in presence_df_coordinates.iterrows():
    print(f"Finding {index}")
    presence_lat = row["decimalLatitude"]
    presence_lon = row["decimalLongitude"]
    
    # Calculate the distances between the occurrence point and all points in bio_df
    distances = bio_df.apply(
    lambda x: distance.euclidean((x["longitude"], x["latitude"]), (presence_lon, presence_lat)), axis=1
    )
    
    # Find the index of the row with the minimum distance
    closest_index = distances.idxmin()
    
    # Get the corresponding environmental variables from temps_df
    environmental_variables = bio_df.loc[closest_index, bio_df.columns[2:]]
    
    # Add the environmental variables to the occurrence row
    presence_df.loc[index, bio_df.columns[2:]] = environmental_variables
print("complete")
presence_df.to_csv("presence_with_bio.csv", index=False)