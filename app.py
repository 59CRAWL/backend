from flask import Flask, request, jsonify
from flask_cors import CORS
from allocation import allocation
from model import model

app = Flask(__name__)
CORS(app)

@app.route("/ingestor", methods=["POST"])
def ingestor():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']

    # Check if the file has a name and is a CSV file
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'})
        
    predicted_csv = model(file)
    
    corrected_json = allocation(predicted_csv)
        
    return jsonify(corrected_json)
    
    # # Save the uploaded CSV file to a folder
    # file.save(os.path.join('uploads', file.filename))

if __name__ == '__main__':
    app.run(port=5000)