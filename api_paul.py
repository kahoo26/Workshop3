from flask import Flask, request, jsonify
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

app = Flask(__name__)

# Load the iris dataset
iris = load_iris()
X = iris.data
y = iris.target

dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X, y)



@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get model arguments from the request parameters
        input_data = [float(request.args.get(f'feature_{i+1}')) for i in range(4)]

        
        predicted_category_tree = dt_classifier.predict([input_data])[0]

        # Return the prediction as JSON
        return jsonify({
            'predicted_species': int(predicted_category_tree)
        })

    except Exception as e:
        return jsonify({'error': str(e)})
    



if __name__ == '__main__':
    app.run(port=5002, debug=True)
