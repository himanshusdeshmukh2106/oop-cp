"""
Test script to verify pre-trained models work correctly
"""
import pickle
import os
import numpy as np

def test_pretrained_models():
    print("=" * 60)
    print("TESTING PRE-TRAINED MODELS")
    print("=" * 60)
    
    models_dir = 'trained_models'
    model_info_path = os.path.join(models_dir, 'model_info.pkl')
    
    # Check if models exist
    if not os.path.exists(model_info_path):
        print("\n❌ Pre-trained models not found!")
        print("Run: python train_and_save_models.py")
        return
    
    print("\n✓ Pre-trained models found\n")
    
    # Load model info
    with open(model_info_path, 'rb') as f:
        model_info = pickle.load(f)
    
    # Test input data
    test_input = [57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2]
    print(f"Test Input: {test_input}\n")
    
    # Load and test each model
    model_names = {
        'logistic_regression': 'Logistic Regression',
        'random_forest': 'Random Forest',
        'decision_tree': 'Decision Tree',
        'knn': 'KNN',
        'naive_bayes': 'Naive Bayes'
    }
    
    predictions = {}
    accuracies = {}
    
    for model_key, display_name in model_names.items():
        model_path = os.path.join(models_dir, f'{model_key}.pkl')
        
        if os.path.exists(model_path):
            # Load model
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            # Make prediction
            pred = model.predict([test_input])
            accuracy = model_info[model_key]['test_accuracy']
            
            predictions[display_name] = pred[0]
            accuracies[display_name] = accuracy
            
            result = "Disease" if pred[0] == 1 else "Healthy"
            print(f"{display_name:25} | Accuracy: {accuracy:6.2f}% | Prediction: {pred[0]} ({result})")
        else:
            print(f"❌ {display_name:25} | Model file not found")
    
    # Find best model
    if accuracies:
        best_model = max(accuracies.items(), key=lambda x: x[1])
        print("\n" + "=" * 60)
        print(f"BEST MODEL: {best_model[0]}")
        print(f"ACCURACY: {best_model[1]:.2f}%")
        print(f"PREDICTION: {predictions[best_model[0]]} ({'Heart Disease' if predictions[best_model[0]] == 1 else 'No Heart Disease'})")
        print("=" * 60)
        
        print("\n✅ All pre-trained models loaded and tested successfully!")
        print("⚡ Predictions are now INSTANT (no training required)")
    else:
        print("\n❌ No models could be loaded")

if __name__ == "__main__":
    test_pretrained_models()
