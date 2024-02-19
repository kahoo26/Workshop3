from flask import Flask, request, jsonify
import requests

agreg = Flask(__name__)

# Ngrok URLs for the two models' APIs
ngrok_url_knn = " https://3ea5-89-30-29-68.ngrok-free.app" 
ngrok_url_reg = "https://ab27-89-30-29-68.ngrok-free.app"  
ngrok_url_svc = "https://0091-89-30-29-68.ngrok-free.app"
ngrok_url_tree = "https://c045-89-30-29-68.ngrok-free.app"

weight_knn = 1.0/3.0
weight_tree = 1.0/3.0
weight_svc = 1.0/3.0

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

        #We signify that we use the global variables for weights.
        global weight_knn
        global weight_tree
        global weight_svc

        # Combine or aggregate the predictions (for example, take the average). Take the weighed sum.
        consensus_prediction = predicted_category_knn*weight_knn + predicted_category_svc*weight_svc + predicted_category_tree*weight_tree

        #Response value is 0, 1 or 2 so the absolute difference between 2 responses is 0, 1 or 2.
        #We multiply each weight by 1, 0.9 or 0.8 depending on the error
        weight_knn = weight_knn * (1.0 - float(abs(predicted_category_knn - consensus_prediction)))
        weight_tree = weight_tree * (1.0 - float(abs(predicted_category_tree - consensus_prediction)))
        weight_svc = weight_svc * (1.0 - float(abs(predicted_category_svc - consensus_prediction)))

        #We need to keep the sum of weights as 1
        sweights = weight_knn + weight_tree + weight_svc
        weight_knn = weight_knn / sweights
        weight_svc = weight_svc / sweights
        weight_tree = weight_tree / sweights

        # Return the consensus prediction as JSON
        return jsonify({'consensus_prediction': consensus_prediction,
                        'prediction svc': predicted_category_svc,
                        'prediction Decision tree': predicted_category_tree,
                        'prediction linear knn': predicted_category_knn})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    agreg.run(port = 5001,debug=True)
