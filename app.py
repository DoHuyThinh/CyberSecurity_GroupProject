from flask import Flask, request, jsonify, render_template, Response, send_from_directory
import pickle
import numpy as np

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
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Read model và scaler
        with open('server_vulnerability_model.pkl', 'rb') as f:
            model, scaler = pickle.load(f)
            
        features = np.array([[
            float(request.json['feature1']),
            float(request.json['feature2']),
            float(request.json['feature3'])
        ]])
        
        # Normalize input data
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/train', methods=['POST'])
def train():
    try:
        import train_model
        return jsonify({
            'message': 'The model has been trained successfully.!'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/style.css')
def serve_css():
    with open('templates/style.css', 'r') as f:
        css_content = f.read()
    return Response(css_content, mimetype='text/css')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
