from flask import Flask, request, jsonify
from flask_cors import CORS
from allocation import allocation
from model import model
from chat import csv_agent

app = Flask(__name__)
CORS(app)

@app.route("/ingestor", methods=["POST"])
def ingestor():
    # Check if a file is included in the request
    if 'file' not in request.files:
        with open('mockData/port_mock_data.csv', 'r') as file:
            predicted_df = model(file)
        
            corrected_json = allocation(predicted_df)
                
            return jsonify(corrected_json)
    else:
        file = request.files['file']

        # Check if the file has a name and is a CSV file
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'})
            
        predicted_df = model(file)
        
        corrected_json = allocation(predicted_df)

        return jsonify(corrected_json)
    
        # # Save the uploaded CSV file to a folder
        # file.save(os.path.join('uploads', file.filename))

@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json()

    return csv_agent(body.get("json"), prompt=body.get("prompt"))
    
if __name__ == '__main__':
    app.run(port=5000)