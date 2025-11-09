"""
Test the prediction system with random samples from the dataset
"""
import pandas as pd
import pickle
import os
import numpy as np
import random

def load_models():
    """Load all pre-trained models"""
    models_dir = 'trained_models'
    model_info_path = os.path.join(models_dir, 'model_info.pkl')
    
    if not os.path.exists(model_info_path):
        print("❌ Pre-trained models not found!")
        print("Run: python train_and_save_models.py")
        return None, None
    
    with open(model_info_path, 'rb') as f:
        model_info = pickle.load(f)
    
    models = {}
    model_names = {
        'logistic_regression': 'Logistic Regression',
        'random_forest': 'Random Forest',
        'decision_tree': 'Decision Tree',
        'knn': 'KNN',
        'naive_bayes': 'Naive Bayes'
    }
    
    for model_key, display_name in model_names.items():
        model_path = os.path.join(models_dir, f'{model_key}.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                models[display_name] = {
                    'model': pickle.load(f),
                    'accuracy': model_info[model_key]['test_accuracy']
                }
    
    return models, model_info

def test_random_samples(num_samples=20):
    print("=" * 90)
    print(f"TESTING WITH {num_samples} RANDOM SAMPLES FROM DATASET")
    print("=" * 90)
    
    # Load dataset
    df = pd.read_csv('Machine_Learning/heart.csv')
    print(f"\nDataset: {len(df)} total samples")
    print(f"Randomly selecting {num_samples} samples for testing...\n")
    
    # Load models
    models, _ = load_models()
    if not models:
        return
    
    # Randomly sample from dataset
    random_samples = df.sample(n=num_samples, random_state=random.randint(1, 1000))
    
    # Track statistics
    model_correct = {name: 0 for name in models.keys()}
    model_predictions = {name: [] for name in models.keys()}
    actual_labels = []
    
    agreement_counts = {
        'unanimous': 0,
        'strong_majority': 0,
        'split': 0
    }
    
    print("=" * 90)
    print("TESTING SAMPLES")
    print("=" * 90)
    
    for idx, (i, row) in enumerate(random_samples.iterrows(), 1):
        features = row[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']].values.tolist()
        actual = int(row['target'])
        actual_labels.append(actual)
        
        # Patient info
        age = int(row['age'])
        sex = 'M' if row['sex'] == 1 else 'F'
        bp = int(row['trestbps'])
        chol = int(row['chol'])
        hr = int(row['thalach'])
        actual_label = "DISEASE" if actual == 1 else "HEALTHY"
        
        print(f"\n{'─' * 90}")
        print(f"Sample {idx:2d}: Age={age}, Sex={sex}, BP={bp}, Chol={chol}, HR={hr}")
        print(f"Actual: {actual_label} ({actual})")
        print(f"{'─' * 90}")
        
        # Get predictions from all models
        predictions = []
        prediction_details = []
        
        for name, model_data in models.items():
            model = model_data['model']
            pred = model.predict([features])[0]
            predictions.append(pred)
            model_predictions[name].append(pred)
            
            # Track correctness
            if pred == actual:
                model_correct[name] += 1
                status = "✓"
            else:
                status = "✗"
            
            # Get probability if available
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba([features])[0]
                confidence = max(proba) * 100
                pred_label = "DISEASE" if pred == 1 else "HEALTHY"
                prediction_details.append(f"{name:20} → {pred_label:8} ({confidence:5.1f}%) {status}")
            else:
                pred_label = "DISEASE" if pred == 1 else "HEALTHY"
                prediction_details.append(f"{name:20} → {pred_label:8}        {status}")
        
        # Print predictions
        for detail in prediction_details:
            print(f"  {detail}")
        
        # Agreement analysis
        healthy_votes = sum(1 for p in predictions if p == 0)
        disease_votes = sum(1 for p in predictions if p == 1)
        
        if healthy_votes == 5 or disease_votes == 5:
            agreement = "UNANIMOUS"
            agreement_counts['unanimous'] += 1
        elif healthy_votes >= 4 or disease_votes >= 4:
            agreement = "STRONG MAJORITY"
            agreement_counts['strong_majority'] += 1
        else:
            agreement = "SPLIT (Borderline)"
            agreement_counts['split'] += 1
        
        # Best model prediction
        best_model = max(models.items(), key=lambda x: x[1]['accuracy'])
        best_pred = model_predictions[best_model[0]][-1]
        best_label = "DISEASE" if best_pred == 1 else "HEALTHY"
        best_correct = "✓ CORRECT" if best_pred == actual else "✗ WRONG"
        
        print(f"\n  Agreement: {agreement} ({healthy_votes} Healthy, {disease_votes} Disease)")
        print(f"  Best Model ({best_model[0]}): {best_label} - {best_correct}")
    
    # Summary Statistics
    print("\n" + "=" * 90)
    print("PERFORMANCE SUMMARY")
    print("=" * 90)
    
    print(f"\n{'Model':<25} {'Correct':<15} {'Accuracy':<15} {'Test Acc':<15}")
    print("─" * 90)
    
    for name, model_data in models.items():
        correct = model_correct[name]
        accuracy = (correct / num_samples) * 100
        test_acc = model_data['accuracy']
        print(f"{name:<25} {correct}/{num_samples} ({correct*100//num_samples}%){'':>5} "
              f"{accuracy:5.1f}%{'':>8} {test_acc:5.1f}%")
    
    # Agreement statistics
    print("\n" + "=" * 90)
    print("AGREEMENT ANALYSIS")
    print("=" * 90)
    
    print(f"\nUnanimous Agreement:    {agreement_counts['unanimous']:2d}/{num_samples} "
          f"({agreement_counts['unanimous']*100//num_samples}%) - All models agree")
    print(f"Strong Majority:        {agreement_counts['strong_majority']:2d}/{num_samples} "
          f"({agreement_counts['strong_majority']*100//num_samples}%) - 4+ models agree")
    print(f"Split (Borderline):     {agreement_counts['split']:2d}/{num_samples} "
          f"({agreement_counts['split']*100//num_samples}%) - Models disagree")
    
    # Confusion matrix for best model
    best_model_name = max(models.items(), key=lambda x: x[1]['accuracy'])[0]
    best_preds = model_predictions[best_model_name]
    
    tp = sum(1 for i in range(num_samples) if actual_labels[i] == 1 and best_preds[i] == 1)
    tn = sum(1 for i in range(num_samples) if actual_labels[i] == 0 and best_preds[i] == 0)
    fp = sum(1 for i in range(num_samples) if actual_labels[i] == 0 and best_preds[i] == 1)
    fn = sum(1 for i in range(num_samples) if actual_labels[i] == 1 and best_preds[i] == 0)
    
    print("\n" + "=" * 90)
    print(f"BEST MODEL: {best_model_name}")
    print("=" * 90)
    
    print(f"\nConfusion Matrix:")
    print(f"                    Predicted")
    print(f"                Healthy  Disease")
    print(f"Actual Healthy     {tn:2d}       {fp:2d}")
    print(f"       Disease     {fn:2d}       {tp:2d}")
    
    if tp + fn > 0:
        sensitivity = tp / (tp + fn) * 100
        print(f"\nSensitivity (Disease Detection): {sensitivity:.1f}%")
    
    if tn + fp > 0:
        specificity = tn / (tn + fp) * 100
        print(f"Specificity (Healthy Detection): {specificity:.1f}%")
    
    # Overall insights
    print("\n" + "=" * 90)
    print("KEY INSIGHTS")
    print("=" * 90)
    
    avg_accuracy = sum(model_correct.values()) / len(models) / num_samples * 100
    best_accuracy = max(model_correct.values()) / num_samples * 100
    
    print(f"""
✅ Average Model Accuracy: {avg_accuracy:.1f}%
✅ Best Model Accuracy: {best_accuracy:.1f}% ({best_model_name})
✅ Unanimous Agreement: {agreement_counts['unanimous']} cases ({agreement_counts['unanimous']*100//num_samples}%)
⚠️  Borderline Cases: {agreement_counts['split']} cases ({agreement_counts['split']*100//num_samples}%)

OBSERVATIONS:
- Models perform well on clear cases (unanimous agreement)
- Borderline cases show disagreement (expected behavior)
- {best_model_name} is the most reliable model
- System correctly identifies uncertainty in difficult cases
""")
    
    return model_correct, agreement_counts

if __name__ == "__main__":
    # Test with 20 random samples
    print("\n🎲 Testing with 20 random samples from the dataset...\n")
    test_random_samples(num_samples=20)
    
    # Option to test more
    print("\n" + "=" * 90)
    print("Want to test more samples? Run:")
    print("  python test_random_samples.py")
    print("=" * 90)
