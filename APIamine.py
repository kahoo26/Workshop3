#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 18:05:20 2024

@author: rais
"""

from sklearn import datasets

iris = datasets.load_iris()
from sklearn.model_selection import train_test_split

import pandas as pd
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()

# Create a DataFrame from the feature data
X = pd.DataFrame(iris.data, columns=iris.feature_names)

# Create a Series from the target variable
y = pd.Series(iris.target, name='target')



# Assuming X contains your features and y contains your target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.svm import LinearSVC

model = LinearSVC()

model.fit(X_train, y_train)

predictions = model.predict(X_test)



import joblib

joblib.dump(model, 'your_model_file.pkl')

from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('your_model_file.pkl')

@app.route('/predict', methods=['GET'])
def predict():
    input_data = [float(request.args.get(f'feature_{i+1}')) for i in range(4)]
    # Make a prediction using the loaded model
    prediction = model.predict([input_data])[0]

    # Map the numeric prediction to the corresponding Iris species

    return jsonify({'predicted_species': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)
    

