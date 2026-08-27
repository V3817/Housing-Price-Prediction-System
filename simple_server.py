"""
Simple Flask Server for Housing Price Prediction
This server loads the trained model and provides a REST API for predictions.
"""

from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to store the model
model = None

def load_model():
    """Load the trained model from the MLflow artifacts."""
    global model
    
    # Path to the trained model
    model_path = "./mlruns/0/d1be49444ebc4c37a69488da5777f496/artifacts/model/model.pkl"
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded successfully from {model_path}")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy", 
        "model_loaded": model is not None,
        "message": "Housing Price Prediction Server is running"
    })

@app.route('/invocations', methods=['POST'])
def predict():
    """Main prediction endpoint that matches MLflow's expected format."""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get the input data
        data = request.get_json()
        
        if 'dataframe_records' not in data:
            return jsonify({"error": "Missing 'dataframe_records' in request"}), 400
        
        # Convert to DataFrame
        input_df = pd.DataFrame(data['dataframe_records'])
        
        # Make prediction
        prediction = model.predict(input_df)
        
        # Return the prediction in MLflow format
        return jsonify({"predictions": prediction.tolist()})
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_simple():
    """Simplified prediction endpoint for direct use."""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get the input data
        data = request.get_json()
        
        # Convert to DataFrame
        input_df = pd.DataFrame([data])
        
        # Make prediction
        log_price = model.predict(input_df)[0]
        
        # Convert from log1p to actual price
        price = round(np.exp(log_price) - 1)
        
        return jsonify({
            "log_prediction": log_price,
            "predicted_price": price,
            "predicted_price_formatted": f"${price:,.2f}"
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "message": "Housing Price Prediction API",
        "endpoints": {
            "GET /health": "Health check",
            "POST /invocations": "MLflow-compatible prediction endpoint",
            "POST /predict": "Simple prediction endpoint",
            "GET /": "This help message"
        },
        "usage": {
            "invocations": "Send data in format: {'dataframe_records': [{'feature1': value1, ...}]}",
            "predict": "Send data in format: {'feature1': value1, 'feature2': value2, ...}"
        }
    })

if __name__ == '__main__':
    logger.info("Starting Housing Price Prediction Server...")
    
    # Load the model
    if load_model():
        logger.info("Server will be available at: http://127.0.0.1:8000")
        logger.info("Press Ctrl+C to stop the server")
        
        # Start the server
        app.run(host='127.0.0.1', port=8000, debug=False)
    else:
        logger.error("Failed to load model. Server cannot start.")
        exit(1)
