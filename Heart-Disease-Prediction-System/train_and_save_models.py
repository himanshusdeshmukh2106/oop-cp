"""
Train all 5 ML models and save them as pickle files
Run this script once to create the trained models
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def train_and_save_models():
    print("=" * 60)
    print("TRAINING AND SAVING ML MODELS")
    print("=" * 60)
    
    # Load the dataset
    df = pd.read_csv('Machine_Learning/heart.csv')
    print(f"\nDataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
    
    # Prepare data
    X = df[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=123, stratify=y)
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples\n")
    
    # Initialize models
    models = {
        'logistic_regression': LogisticRegression(max_iter=1000),
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=123),
        'decision_tree': DecisionTreeClassifier(criterion='entropy', random_state=123),
        'knn': KNeighborsClassifier(n_neighbors=7),
        'naive_bayes': GaussianNB()
    }
    
    # Create models directory if it doesn't exist
    models_dir = 'trained_models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created directory: {models_dir}/\n")
    
    # Train and save each model
    model_info = {}
    
    for name, model in models.items():
        print(f"Training {name.replace('_', ' ').title()}...")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Calculate accuracy
        train_accuracy = model.score(X_train, y_train) * 100
        test_accuracy = model.score(X_test, y_test) * 100
        
        # Save the model
        model_path = os.path.join(models_dir, f'{name}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Store info
        model_info[name] = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'path': model_path
        }
        
        print(f"  ✓ Train Accuracy: {train_accuracy:.2f}%")
        print(f"  ✓ Test Accuracy: {test_accuracy:.2f}%")
        print(f"  ✓ Saved to: {model_path}\n")
    
    # Save model info
    info_path = os.path.join(models_dir, 'model_info.pkl')
    with open(info_path, 'wb') as f:
        pickle.dump(model_info, f)
    
    print("=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    
    # Find best model
    best_model = max(model_info.items(), key=lambda x: x[1]['test_accuracy'])
    print(f"\nBest Model: {best_model[0].replace('_', ' ').title()}")
    print(f"Test Accuracy: {best_model[1]['test_accuracy']:.2f}%")
    
    print(f"\nAll models saved in: {models_dir}/")
    print("\nFiles created:")
    for name in models.keys():
        print(f"  - {name}.pkl")
    print(f"  - model_info.pkl")
    
    return model_info

if __name__ == "__main__":
    train_and_save_models()
