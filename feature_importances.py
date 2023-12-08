# Import necessary libraries and functions
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split

# Read the CSV data and select relevant columns
data = pd.read_csv('current_data.csv') 
selected_columns = ['Longitude', 'Latitude', 'Presence', "bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19","gdd10","ngd10"]
data = data[selected_columns]

# Split the data into features (bio1-bio9) and target (presence)
X = data[['Longitude', 'Latitude', "bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19","gdd10","ngd10"]]
y = data['Presence']

# Separate the environmental features from latitude and longitude
bios = X[["bio1","bio2","bio3","bio4","bio5","bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19","gdd10","ngd10"]]
lat_lon = X[['Longitude', 'Latitude']]

# Standardize the environmental features
scaler_bio = StandardScaler()
bios_scaled = scaler_bio.fit_transform(bios)
X_scaled = pd.concat([lat_lon, pd.DataFrame(bios_scaled, columns=bios.columns)], axis=1)

# Split the data into a training set and a testing set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Ensure that the shapes of X_train, X_test, y_train, y_test are correct
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)
# Create the RandomForestClassifier with specified parameters
rf_classifier = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=42
)

# Train the RandomForestClassifier
rf_classifier.fit(X_train, y_train)

# Get feature importances
feature_importances = rf_classifier.feature_importances_

# Create a DataFrame to associate feature names with their importances
importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Print or visualize the feature importances
print(importance_df)

# Plotting feature importances
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.title('Feature Importances')
plt.show()
