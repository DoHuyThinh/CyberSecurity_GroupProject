import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle


data = pd.read_csv("server_metrics_data.csv")


X = data[['feature1', 'feature2', 'feature3']]  
y = (data['label'] == 'normal').astype(int)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.2%}")

with open("server_vulnerability_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model has been saved to server_vulnerability_model.pkl")
