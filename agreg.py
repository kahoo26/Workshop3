from flask import Flask, request, jsonify
import requests

agreg = Flask(__name__)

# Ngrok URLs for the two models' APIs
ngrok_url_knn = " https://3ea5-89-30-29-68.ngrok-free.app" 
ngrok_url_reg = "https://ab27-89-30-29-68.ngrok-free.app"  
ngrok_url_svc = "https://0091-89-30-29-68.ngrok-free.app"
ngrok_url_tree = "https://c045-89-30-29-68.ngrok-free.app"

@agreg.route('/predict', methods=['GET'])
def predict_aggregator():
    try:
        # Get model arguments from the request parameters
        input_data = [float(request.args.get(f'feature_{i+1}')) for i in range(4)]

        # Make a request to your model's API
        response_knn = requests.get(f'{ngrok_url_knn}/predict', params={'feature_1': input_data[0], 'feature_2': input_data[1], 'feature_3': input_data[2], 'feature_4': input_data[3]})
        data_knn = response_knn.json()
        predicted_category_knn = data_knn['predicted_species']
        
        response_tree = requests.get(f'{ngrok_url_tree}/predict', params={'feature_1': input_data[0], 'feature_2': input_data[1], 'feature_3': input_data[2], 'feature_4': input_data[3]})
        data_tree = response_tree.json()
        predicted_category_tree = data_tree['predicted_species']
        
        response_svc = requests.get(f'{ngrok_url_svc}/predict', params={'feature_1': input_data[0], 'feature_2': input_data[1], 'feature_3': input_data[2], 'feature_4': input_data[3]})
        data_svc = response_svc.json()
        predicted_category_svc = data_svc['predicted species']

        
        #response_reg = requests.get(f'{ngrok_url_reg}/predict', params={'feature_1': input_data[0], 'feature_2': input_data[1], 'feature_3': input_data[2], 'feature_4': input_data[3]})
        #data_reg = response_reg.json()
        #predicted_category_reg = data_reg['predicted_species']

        # Combine or aggregate the predictions (for example, take the average)
        consensus_prediction = (predicted_category_knn + predicted_category_svc + predicted_category_tree) / 3

        # Return the consensus prediction as JSON
        return jsonify({'consensus_prediction': consensus_prediction,
                        'prediction svc': predicted_category_svc,
                        'prediction Decision tree': predicted_category_tree,
                        'prediction linear knn': predicted_category_knn})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    agreg.run(port = 5001,debug=True)
