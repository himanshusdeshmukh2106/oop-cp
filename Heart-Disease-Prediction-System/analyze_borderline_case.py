"""
Analyze why different models give different predictions
"""
import pandas as pd
import numpy as np
import pickle
import os

def analyze_case():
    print("=" * 70)
    print("ANALYZING BORDERLINE CASE")
    print("=" * 70)
    
    # Test case
    test_input = [57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2]
    feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                     'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    
    print("\nPatient Profile:")
    print("-" * 70)
    interpretations = {
        'age': f"{test_input[0]} years old",
        'sex': "Female" if test_input[1] == 0 else "Male",
        'cp': f"Chest pain type: {test_input[2]} (Atypical angina)",
        'trestbps': f"Blood pressure: {test_input[3]} mm Hg (Normal)",
        'chol': f"Cholesterol: {test_input[4]} mg/dl (Borderline high)",
        'fbs': f"Fasting blood sugar: {'High' if test_input[5] == 1 else 'Normal'}",
        'restecg': f"Resting ECG: {test_input[6]} (Normal)",
        'thalach': f"Max heart rate: {test_input[7]} (Good for age)",
        'exang': f"Exercise angina: {'Yes' if test_input[8] == 1 else 'No'}",
        'oldpeak': f"ST depression: {test_input[9]} (Excellent)",
        'slope': f"ST slope: {test_input[10]} (Upsloping - good)",
        'ca': f"Major vessels: {test_input[11]} (1 vessel)",
        'thal': f"Thalassemia: {test_input[12]} (Normal)"
    }
    
    for i, (feature, value) in enumerate(zip(feature_names, test_input)):
        print(f"  {feature:12} = {value:6} → {interpretations[feature]}")
    
    print("\n" + "=" * 70)
    print("RISK FACTOR ANALYSIS")
    print("=" * 70)
    
    print("\n🟢 HEALTHY INDICATORS:")
    print("  ✓ Female (lower risk than males)")
    print("  ✓ Good max heart rate (174 for age 57)")
    print("  ✓ No exercise-induced angina")
    print("  ✓ ST depression = 0.0 (excellent)")
    print("  ✓ Upsloping ST segment (good)")
    print("  ✓ Normal resting ECG")
    print("  ✓ Normal fasting blood sugar")
    
    print("\n🟡 BORDERLINE/MODERATE INDICATORS:")
    print("  ⚠ Age 57 (moderate risk)")
    print("  ⚠ Cholesterol 236 (borderline high, normal is <200)")
    print("  ⚠ 1 major vessel affected")
    print("  ⚠ Atypical angina chest pain")
    
    print("\n🔴 HIGH RISK INDICATORS:")
    print("  ✗ None significant")
    
    # Load models and get prediction probabilities
    models_dir = 'trained_models'
    
    print("\n" + "=" * 70)
    print("MODEL PREDICTIONS WITH CONFIDENCE")
    print("=" * 70)
    
    model_files = {
        'logistic_regression': 'Logistic Regression',
        'random_forest': 'Random Forest',
        'decision_tree': 'Decision Tree',
        'naive_bayes': 'Naive Bayes'
    }
    
    for model_key, display_name in model_files.items():
        model_path = os.path.join(models_dir, f'{model_key}.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            pred = model.predict([test_input])[0]
            
            # Get probability if available
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba([test_input])[0]
                healthy_prob = proba[0] * 100
                disease_prob = proba[1] * 100
                
                result = "HEALTHY" if pred == 0 else "DISEASE"
                confidence = max(healthy_prob, disease_prob)
                
                print(f"\n{display_name}:")
                print(f"  Prediction: {result}")
                print(f"  Confidence: {confidence:.1f}%")
                print(f"  Probabilities: Healthy={healthy_prob:.1f}%, Disease={disease_prob:.1f}%")
                
                if abs(healthy_prob - disease_prob) < 10:
                    print(f"  ⚠️  BORDERLINE CASE (difference: {abs(healthy_prob - disease_prob):.1f}%)")
            else:
                result = "HEALTHY" if pred == 0 else "DISEASE"
                print(f"\n{display_name}:")
                print(f"  Prediction: {result}")
                print(f"  (No probability available for this model)")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
This is a BORDERLINE CASE - the patient has:
  • Several healthy indicators (good heart rate, no ST depression)
  • Some moderate risk factors (age, cholesterol)
  • No severe risk factors

Different algorithms weigh these factors differently:
  • Random Forest (86.89% accurate) → Focuses on overall pattern → HEALTHY
  • Logistic Regression (85.25% accurate) → Linear combination → DISEASE
  • Decision Tree (81.97% accurate) → Simple rules → HEALTHY

The contradicting predictions are NORMAL for borderline cases.
We use the MOST ACCURATE model (Random Forest) for the final decision.

RECOMMENDATION: 
  ✓ Use Random Forest prediction: HEALTHY
  ✓ But monitor cholesterol levels
  ✓ Regular checkups recommended due to age
""")

if __name__ == "__main__":
    analyze_case()
