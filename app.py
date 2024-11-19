from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Declare global model variable
model = None

# Load the trained model from file
def load_model():
    global model
    try:
        with open("new_intrusion_model.pkl", "rb") as file:
            model = pickle.load(file)
    except FileNotFoundError:
        model = None

# Call the load_model function when the app starts
load_model()

@app.route('/')
def home():
    return "Welcome to the Secured Cloud Application!"

@app.route('/predict', methods=['POST'])
def predict():
    global model
    try:
        data = request.get_json()
        if not all(feature in data for feature in ['feature1', 'feature2', 'feature3']):
            return jsonify({"error": "Missing required features"}), 400

        input_data = [data['feature1'], data['feature2'], data['feature3']]

        if model is None:
            return jsonify({"error": "Model not loaded. Please train the model first"}), 400

        prediction = model.predict([input_data])
        return jsonify({"prediction": prediction[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train', methods=['POST'])
def train_model():
    global model
    try:
        # Read the data
        data = pd.read_csv("sample_data.csv")
        
        # Separate features and label
        features = ['feature1', 'feature2', 'feature3']
        X = data[features]  # Explicitly specify feature names
        y = data['label']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train with feature names
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the model
        with open("new_intrusion_model.pkl", "wb") as file:
            pickle.dump(model, file)

        accuracy = model.score(X_test, y_test)
        return jsonify({
            "message": "Model trained successfully!",
            "accuracy": float(accuracy)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
