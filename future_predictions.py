# Import necessary libraries and functions
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib

# Read the CSV data and select relevant columns
data = pd.read_csv('future_combined_data/2100/2100_ssp126_cleaned_data.csv') 
selected_columns = ['Longitude', 'Latitude',"bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19"]
data = data[selected_columns]

X = data[['Longitude', 'Latitude', "bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19"]]

# Select the relevant columns
# Separate the environmental features from latitude and longitude
# Standardize the environmental features
# Combine the scaled environmental features with latitude and longitude
bios = X[["bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19"]]
lat_lon = X[['Longitude', 'Latitude']]
scaler_bio = StandardScaler()
bios_scaled = scaler_bio.fit_transform(bios)
X_scaled = pd.concat([lat_lon, pd.DataFrame(bios_scaled, columns=bios.columns)], axis=1)

# Load the trained model
filename = 'Sf_rfr_model.sav'
rfr_model = joblib.load(filename)

predictions = rfr_model.predict(X_scaled)

# Create a DataFrame with longitude, latitude, and presence columns
result_df = pd.DataFrame({'longitude': data['Longitude'], 'latitude': data['Latitude'], 'presence': predictions})
# Filter rows where 'presence' column is equal to 1
filtered_df = result_df[result_df['presence'] == 1]
# Check if there are any rows with presence equal to 1
if not filtered_df.empty:
    # Write the filtered DataFrame to a CSV file
    filtered_df.to_csv('future_combined_data/2100/2100_ssp126_predictions.csv', index=False)
    print("Predictions with presence equal to 1 have been written to presence_predictions.csv")
else:
    print("No predictions with presence equal to 1 found.")
