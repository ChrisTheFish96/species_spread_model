# Import necessary libraries and functions
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib

# Read the CSV data and select relevant columns
data = pd.read_csv('data_files/shuffled_train_test_pa_data.csv') 
selected_columns = ['Longitude', 'Latitude', 'Presence', "bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19"]
data = data[selected_columns]

# Split the data into features (bio1-bio9) and target (presence)
X = data[['Longitude', 'Latitude', "bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19"]]
y = data['Presence']

# Select the relevant columns
# Separate the environmental features from latitude and longitude
# Standardize the environmental features
# Combine the scaled environmental features with latitude and longitude
bios = X[["bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19"]]
lat_lon = X[['Longitude', 'Latitude']]
scaler_bio = StandardScaler()
bios_scaled = scaler_bio.fit_transform(bios)
X_scaled = pd.concat([lat_lon, pd.DataFrame(bios_scaled, columns=bios.columns)], axis=1)

# Split the data into a training set and a testing set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Create a RandomForestClassifier
rf_classifier = RandomForestClassifier(random_state=42)

# Define a parameter grid to search over
param_grid = {
    'n_estimators': [200, 300, 600],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}

# Create the GridSearchCV object
grid_search = GridSearchCV(rf_classifier, param_grid, cv=5, scoring='accuracy')

# Fit the model with the grid search
grid_search.fit(X_train, y_train)

# Get the best hyperparameters
best_params = grid_search.best_params_
print(best_params)
# Train a model with the best hyperparameters
best_rf_classifier = RandomForestClassifier(random_state=42, **best_params)
best_rf_classifier.fit(X_train, y_train)

# Save the trained model to a file
filename = 'Sf_rfr_model.sav'
joblib.dump(best_rf_classifier, filename)

# Make predictions on the test data
y_pred = best_rf_classifier.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Best Hyperparameters:", best_params)
print(f"Accuracy: {accuracy:.4f}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(classification_rep)