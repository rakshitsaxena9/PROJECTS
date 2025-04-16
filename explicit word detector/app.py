from flask import Flask, request, jsonify
from model.bert_model import BertModel
from utils import pre_processing_data,postprocess
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Get configurations from environment variables
MODEL_PATH = os.getenv('MODEL_PATH')
TOKENIZER_PATH = os.getenv('TOKENIZER_PATH')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Load the BERT model and tokenizer
model = BertModel(MODEL_PATH, TOKENIZER_PATH)
print('MODEL Loaded..............................................')
@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get input data
        input_data = request.get_json()
        
        # Assume input_data is a list of texts for prediction
        processed_data = pre_processing_data(input_data['string'])
        
        # Make predictions
        predictions = model.prediction(processed_data)
        
        # Postprocess results
        result = postprocess(predictions)
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'status':None,'error': str(e)}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # app.run()
    processed_data = pre_processing_data('you m*therf@cker.')
    # Make predictions
    predictions = model.prediction(processed_data)
    result = postprocess(predictions)
    print(result)

        


