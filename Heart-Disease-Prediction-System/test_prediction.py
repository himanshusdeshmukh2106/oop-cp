"""
Test script for the updated heart disease prediction function
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def test_prediction():
    # Load the dataset
    df = pd.read_csv('Machine_Learning/heart.csv')
    
    # Sample input data (same as in the original notebook)
    # Format: [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    test_input = [57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2]
    
    X = df[['age','sex','cp',  'trestbps',  'chol',  'fbs',  'restecg',  'thalach',  'exang',  'oldpeak',  'slope',  'ca',  'thal']]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=123, stratify=y)
    
    # Initialize multiple models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=123),
        'Decision Tree': DecisionTreeClassifier(criterion='entropy', random_state=123),
        'KNN': KNeighborsClassifier(n_neighbors=7),
        'Naive Bayes': GaussianNB()
    }
    
    # Train all models and get predictions
    predictions = {}
    accuracies = {}
    
    print("=" * 60)
    print("HEART DISEASE PREDICTION - MULTIPLE ALGORITHMS")
    print("=" * 60)
    print(f"\nTest Input: {test_input}\n")
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict([test_input])
        accuracy = model.score(X_test, y_test) * 100
        predictions[name] = pred[0]
        accuracies[name] = accuracy
        print(f"{name:25} | Accuracy: {accuracy:6.2f}% | Prediction: {pred[0]} ({'Disease' if pred[0] == 1 else 'Healthy'})")
    
    # Use the model with highest accuracy
    best_model_name = max(accuracies, key=accuracies.get)
    best_accuracy = accuracies[best_model_name]
    final_prediction = predictions[best_model_name]
    
    print("\n" + "=" * 60)
    print(f"BEST MODEL: {best_model_name}")
    print(f"ACCURACY: {best_accuracy:.2f}%")
    print(f"FINAL PREDICTION: {final_prediction} ({'Heart Disease Detected' if final_prediction == 1 else 'No Heart Disease'})")
    print("=" * 60)

if __name__ == "__main__":
    test_prediction()
