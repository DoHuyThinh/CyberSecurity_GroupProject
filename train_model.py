import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle


data = pd.read_csv("sample_data.csv")


X = data[['feature1', 'feature2', 'feature3']]  
y = data['label'] 


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = RandomForestClassifier()
model.fit(X_train, y_train)


with open("new_intrusion_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model have been saved to intrusion_model.pkl")
