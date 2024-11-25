from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

# Read and shuffle data
data = pd.read_csv('server_metrics_data.csv')
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Split features and label
X = data[['feature1', 'feature2', 'feature3']]
y = data['label']

# Normalize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data with stratification to ensure balance
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# RandomForest with parameters
model = RandomForestClassifier(
    n_estimators=200,          
    max_depth=4,               
    min_samples_split=10,      
    min_samples_leaf=4,        
    max_features='sqrt',
    class_weight='balanced',
    random_state=42
)

# Define grid search
param_grid = {
    'max_depth': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'min_samples_leaf': [3, 4, 5]
}

# Find best parameters and train
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
model = grid_search.best_estimator_

# Save model and scaler
with open('server_vulnerability_model.pkl', 'wb') as f:
    pickle.dump((model, scaler), f)

print("Model has been trained and saved successfully!")
