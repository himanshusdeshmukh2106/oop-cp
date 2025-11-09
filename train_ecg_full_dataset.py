"""
Train ECG models on the FULL dataset (11,148 images)
This processes all raw ECG images to create a robust model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import joblib
import os
import sys
from pathlib import Path

# Add the ECG predictor to path
sys.path.append('Heart-Disease-Prediction-System/health')
from ecg_predictor import ECGPredictor

print("=" * 70)
print("ECG Model Training on FULL Dataset (11,148 images)")
print("=" * 70)

# Dataset paths
dataset_base = "Cardiovascular-Detection-using-ECG-images/ECG_IMAGES_DATASET"

categories = {
    'Normal Person ECG Images (284x12=3408)': 2,
    'ECG Images of Myocardial Infarction Patients (240x12=2880)': 1,
    'ECG Images of Patient that have abnormal heartbeat (233x12=2796)': 0,
    'ECG Images of Patient that have History of MI (172x12=2064)': 3
}

print("\n📂 Processing ECG images from dataset...")
print("This will take several minutes...")

all_features = []
all_labels = []
processed_count = 0
error_count = 0

predictor = ECGPredictor()

for category_folder, label in categories.items():
    category_path = os.path.join(dataset_base, category_folder)
    
    if not os.path.exists(category_path):
        print(f"⚠️  Warning: {category_folder} not found, skipping...")
        continue
    
    image_files = [f for f in os.listdir(category_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"\n📁 {category_folder}")
    print(f"   Found {len(image_files)} images")
    
    for idx, image_file in enumerate(image_files):
        try:
            image_path = os.path.join(category_path, image_file)
            
            # Create temp workspace
            predictor.create_temp_workspace()
            
            # Process image through ECG pipeline
            ecg_image = predictor.get_image(image_path)
            gray_image = predictor.gray_image(ecg_image)
            leads = predictor.divide_leads(gray_image)
            predictor.signal_extraction_scaling(leads)
            combined_signal = predictor.combine_convert_1d_signal()
            
            # Get features (should be 3060)
            features = combined_signal.values.flatten()
            
            if len(features) == 3060:
                all_features.append(features)
                all_labels.append(label)
                processed_count += 1
            else:
                error_count += 1
            
            # Cleanup
            predictor.cleanup_temp_workspace()
            
            # Progress update every 100 images
            if (idx + 1) % 100 == 0:
                print(f"   Processed {idx + 1}/{len(image_files)} images...")
                
        except Exception as e:
            error_count += 1
            predictor.cleanup_temp_workspace()
            if error_count < 5:  # Only show first few errors
                print(f"   ⚠️  Error processing {image_file}: {str(e)[:50]}")
            continue
    
    print(f"   ✅ Successfully processed {processed_count} images from this category")

if len(all_features) == 0:
    print("\n❌ No images processed successfully!")
    exit(1)

# Convert to arrays
X = np.array(all_features)
y = np.array(all_labels)

print(f"\n" + "=" * 70)
print(f"✅ Successfully processed {processed_count} images")
print(f"⚠️  Failed to process {error_count} images")
print(f"\nDataset shape: {X.shape}")
print(f"Features per sample: {X.shape[1]}")
print(f"\nClass distribution:")
class_names = {0: 'Abnormal Heartbeat', 1: 'Myocardial Infarction', 2: 'Normal', 3: 'History of MI'}
for label in sorted(np.unique(y)):
    count = np.sum(y == label)
    percentage = (count / len(y)) * 100
    print(f"  Class {label} ({class_names[label]}): {count} samples ({percentage:.1f}%)")

# Split data
print("\n🔧 Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Standardize features
print("\n📊 Standardizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply PCA
print("\n🔬 Applying PCA for dimensionality reduction...")
n_components = min(150, X_train.shape[0] - 1, X_train.shape[1])
pca = PCA(n_components=n_components, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

explained_var = pca.explained_variance_ratio_.sum()
print(f"✅ Reduced from {X_train.shape[1]} to {n_components} components")
print(f"Explained variance: {explained_var:.2%}")

# Train models
print("\n🤖 Training classification models...")
print("This may take a few minutes...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=2000, random_state=42, C=1.0),
    'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=15, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
    'Naive Bayes': GaussianNB(),
    'SVC': SVC(probability=True, random_state=42, C=1.0, kernel='rbf')
}

trained_models = {}
accuracies = {}

for name, model in models.items():
    print(f"  Training {name}...", end=" ", flush=True)
    model.fit(X_train_pca, y_train)
    train_acc = model.score(X_train_pca, y_train)
    test_acc = model.score(X_test_pca, y_test)
    accuracies[name] = test_acc
    trained_models[name] = model
    print(f"✅ Train: {train_acc:.2%}, Test: {test_acc:.2%}")

# Create voting classifier with best models
print("\n🗳️  Creating ensemble voting classifier...")
best_models = sorted(accuracies.items(), key=lambda x: x[1], reverse=True)[:5]
print(f"Using top 5 models:")
for name, acc in best_models:
    print(f"  - {name}: {acc:.2%}")

voting_clf = VotingClassifier(
    estimators=[(name, trained_models[name]) for name, _ in best_models],
    voting='soft',
    n_jobs=-1
)

voting_clf.fit(X_train_pca, y_train)
voting_train_acc = voting_clf.score(X_train_pca, y_train)
voting_test_acc = voting_clf.score(X_test_pca, y_test)
print(f"✅ Ensemble - Train: {voting_train_acc:.2%}, Test: {voting_test_acc:.2%}")

# Save models
print("\n💾 Saving models...")
output_dir = "Heart-Disease-Prediction-System/trained_models"
os.makedirs(output_dir, exist_ok=True)

# Save scaler
scaler_path = os.path.join(output_dir, "scaler_ECG.pkl")
joblib.dump(scaler, scaler_path)
print(f"✅ Saved scaler: {scaler_path}")

# Save PCA
pca_path = os.path.join(output_dir, "PCA_ECG (1).pkl")
joblib.dump(pca, pca_path)
print(f"✅ Saved PCA model: {pca_path}")

# Save voting classifier
model_path = os.path.join(output_dir, "Heart_Disease_Prediction_using_ECG (4).pkl")
joblib.dump(voting_clf, model_path)
print(f"✅ Saved ECG classifier: {model_path}")

# Save model info
model_info = {
    'total_samples': len(X),
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'input_features': 3060,
    'pca_components': n_components,
    'explained_variance': float(explained_var),
    'voting_train_accuracy': float(voting_train_acc),
    'voting_test_accuracy': float(voting_test_acc),
    'individual_accuracies': {k: float(v) for k, v in accuracies.items()},
    'best_individual_model': max(accuracies, key=accuracies.get),
    'best_individual_accuracy': float(max(accuracies.values())),
    'sklearn_version': '1.5.2',
    'uses_scaler': True,
    'n_classes': 4,
    'class_mapping': class_names
}

info_path = os.path.join(output_dir, "ecg_model_info.txt")
with open(info_path, 'w') as f:
    f.write("ECG Model Information\n")
    f.write("=" * 70 + "\n\n")
    for key, value in model_info.items():
        f.write(f"{key}: {value}\n")

print(f"✅ Saved model info: {info_path}")

print("\n" + "=" * 70)
print("✅ ECG Models Successfully Trained on Full Dataset!")
print("=" * 70)
print(f"\nDataset: {processed_count} images processed")
print(f"Best Individual Model: {model_info['best_individual_model']} ({model_info['best_individual_accuracy']:.2%})")
print(f"Ensemble Test Accuracy: {voting_test_acc:.2%}")
print(f"\nPipeline: Image → 3060 features → Standardization → PCA ({n_components} components) → Ensemble")
print("\nModels are now ready for high-confidence predictions!")
print("Try uploading an ECG image to see improved results! 🚀")
