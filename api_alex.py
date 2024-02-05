from sklearn.datasets import load_iris	
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

iris = load_iris(as_frame = True)
x = iris.data
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state = 20, stratify = y)

#We use a svc classifier
svc_classifier = SVC(kernel='linear')
svc_classifier.fit(x_train, y_train)

from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        input_data = np.array([float(request.args.get(f'feature_{i+1}')) for i in range(4)])
        input_data = input_data.reshape(1, -1)
        predict_svc = svc_classifier.predict(input_data)[0]
        return jsonify({'predicted species': int(predict_svc)})
    except Exception as e:
        return jsonify({'error': str(e)})




if __name__ == '__main__':
    app.run(debug=True)


#y_pred = svc_classifier.predict(x_test)
#accuracy = accuracy_score(y_test, y_pred)
#print(f"Accuracy: {accuracy}")

