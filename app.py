from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

model = None

def load_model():
    global model
    try:
        with open("server_vulnerability_model.pkl", "rb") as file:
            model = pickle.load(file)
    except FileNotFoundError:
        model = None

load_model()

@app.route('/')
def home():
    return "Welcome to the Server Vulnerability Analysis API!"

@app.route('/predict', methods=['POST'])
def predict_vulnerability():
    global model
    try:
        data = request.get_json()
        required_features = ['feature1', 'feature2', 'feature3']
        if not all(feature in data for feature in required_features):
            return jsonify({"error": "Missing required features"}), 400
            
        input_data = [
            data['feature1'],
            data['feature2'],
            data['feature3']
        ]
        
        if model is None:
            return jsonify({"error": "Model not loaded. Please train the model first"}), 400
            
        prediction = model.predict([input_data])
        return jsonify({"prediction": "Normal" if prediction[0] == 1 else "Attack"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train', methods=['POST'])
def train_model():
    global model
    try:
      
        data = pd.read_csv("server_metrics_data.csv")
        
        X = data[['feature1', 'feature2', 'feature3']]
        y = (data['label'] == 'normal').astype(int)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
       
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        with open("server_vulnerability_model.pkl", "wb") as file:
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
