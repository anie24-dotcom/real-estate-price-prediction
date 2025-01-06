from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import json
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with the frontend

def load_model():
    # Get the base directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Path for the pickle model file
    model_path = os.path.join(base_dir, '..', 'model', 'bangalore_home_prices_model.pickle')
    # Load the model from the pickle file
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    # Path for columns.json
    columns_path = os.path.join(base_dir, 'columns.json')
    
    # Load the data columns from the columns.json file
    with open(columns_path, 'r') as f:
        data_columns = json.load(f)['data_columns']
    return model, data_columns

# Route to serve the frontend
@app.route('/')
def home():
    return render_template('app.html')

# Endpoint to fetch location names
@app.route('/api/get_location_names', methods=['GET'])
def get_location_names():
    _, data_columns = load_model()
    # Locations start from index 3 in data_columns
    locations = data_columns[3:]
    return jsonify({'locations': locations})

# Endpoint for prediction
@app.route('/api/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.get_json()
        location = data.get('location', '').lower()  # Ensure lowercase for comparison
        sqft = data.get('total_sqft', 0)
        bath = data.get('bath', 0)
        bhk = data.get('bhk', 0)

        model, data_columns = load_model()

        # Prepare input data for prediction
        x = np.zeros(len(data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk

        # Check and set the location index
        loc_index = -1
        if location in data_columns:
            loc_index = data_columns.index(location)
            x[loc_index] = 1

        # Ensure x is a 2D array
        x = x.reshape(1, -1)
        estimated_price = model.predict(x)[0]
        return jsonify({'estimated_price': round(estimated_price, 2)})

    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({'error': 'Prediction failed. Please check input values and try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
