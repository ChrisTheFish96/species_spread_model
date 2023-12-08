# Import necessary libraries and functions
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.neural_network import MLPClassifier
# Read the CSV data and select relevant columns
data = pd.read_csv('filtered_file.csv') 
selected_columns = ["Longitude","Latitude","Presence","bio1","bio6","bio9","bio11","bio12","ngd10","gdd10"
]
data = data[selected_columns]

# Split the data into features (bio1-bio9) and target (presence)
X = data[["Longitude","Latitude","bio1","bio6","bio9","bio11","bio12","ngd10","gdd10"]]
y = data['Presence']

# Select the relevant columns
# Separate the environmental features from latitude and longitude
# Standardize the environmental features
# Combine the scaled environmental features with latitude and longitude
bios = X[["bio1","bio6","bio9","bio11","bio12","ngd10","gdd10"]]
lat_lon = X[['Longitude', 'Latitude']]
scaler_bio = StandardScaler()
bios_scaled = scaler_bio.fit_transform(bios)
X_scaled = pd.concat([lat_lon, pd.DataFrame(bios_scaled, columns=bios.columns)], axis=1)

# Split the data into a training set and a testing set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
# Create the MLPClassifier with specified hyperparameters
ann_classifier = MLPClassifier(
    activation='relu',
    alpha=0.0001,
    hidden_layer_sizes=(100, 50, 25),
    solver='adam',
    random_state=42
)

# Train the ANN
ann_classifier.fit(X_train, y_train)  # Assuming X_train and y_train are your training data

# Make predictions
y_pred_ann = ann_classifier.predict(X_test)  # Assuming X_test is your test data

# Evaluate the performance of the ANN
accuracy_ann = accuracy_score(y_test, y_pred_ann)
conf_matrix_ann = confusion_matrix(y_test, y_pred_ann)
classification_rep_ann = classification_report(y_test, y_pred_ann)

# Print the evaluation metrics
print(f"Accuracy of ANN: {accuracy_ann:.4f}")
print("Confusion Matrix:")
print(conf_matrix_ann)
print("Classification Report:")
print(classification_rep_ann)
