"""
Retrain ECG models from raw images with proper feature extraction
This processes actual ECG images to create the 3060-feature dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import joblib
import os
from pathlib import Path

print("=" * 60)
print("ECG Model Retraining from Pre-processed 1D Signals")
print("=" * 60)

# Load pre-processed 1D signals
preprocessed_path = "Cardiovascular-Detection-using-ECG-images/preprocessed_1d"

if not os.path.exists(preprocessed_path):
    print(f"\n❌ Error: Preprocessed data not found at {preprocessed_path}")
    exit(1)

print("\n📂 Loading preprocessed 1D ECG signals...")

# Categories mapping
categories = {
    'NORMAL': 2,
    'MI': 1,
    'AHB': 0,
    'PM': 3
}

all_data = []
all_labels = []

for category_name, label in categories.items():
    category_path = os.path.join(preprocessed_path, category_name)
    
    if not os.path.exists(category_path):
        print(f"⚠️  Warning: {category_name} folder not found, skipping...")
        continue
    
    csv_files = [f for f in os.listdir(category_path) if f.endswith('.csv')]
    print(f"  {category_name}: Found {len(csv_files)} samples")
    
    for csv_file in csv_files:
        try:
            csv_path = os.path.join(category_path, csv_file)
            # Try reading with and without header
            try:
                df = pd.read_csv(csv_path)
                # Remove target column if exists
                if 'Target' in df.columns or 'target' in df.columns:
                    df = df.drop(columns=['Target', 'target'], errors='ignore')
            except:
                df = pd.read_csv(csv_path, header=None)
            
            # Flatten to 1D if needed
            features = df.values.flatten()
            
            # Ensure we have 3060 features (12 leads × 255 points)
            if len(features) >= 3060:
                features = features[:3060]
            else:
                # Pad with zeros if needed
                features = np.pad(features, (0, 3060 - len(features)), 'constant')
            
            all_data.append(features)
            all_labels.append(label)
            
        except Exception as e:
            print(f"    ⚠️  Error loading {csv_file}: {e}")
            continue

if len(all_data) == 0:
    print("\n❌ No data loaded! Please check the preprocessed_1d directory.")
    exit(1)

# Convert to arrays
X = np.array(all_data)
y = np.array(all_labels)

print(f"\n✅ Loaded {len(X)} samples")
print(f"Features shape: {X.shape}")
print(f"Labels distribution:")
for cat_name, label in categories.items():
    count = np.sum(y == label)
    print(f"  {cat_name} (class {label}): {count} samples")

# Split data
print("\n🔧 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Apply PCA
print("\n🔬 Applying PCA for dimensionality reduction...")
# n_components must be <= min(n_samples, n_features)
max_components = min(X_train.shape[0], X_train.shape[1])
n_components = min(40, max_components)  # Use 40 or less
pca = PCA(n_components=n_components, random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

print(f"✅ Reduced from {X_train.shape[1]} to {n_components} components")
print(f"Explained variance: {pca.explained_variance_ratio_.sum():.2%}")

# Train models
print("\n🤖 Training classification models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=2000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'Naive Bayes': GaussianNB(),
    'SVC': SVC(probability=True, random_state=42)
}

trained_models = {}
accuracies = {}

for name, model in models.items():
    print(f"  Training {name}...", end=" ")
    model.fit(X_train_pca, y_train)
    accuracy = model.score(X_test_pca, y_test)
    accuracies[name] = accuracy
    trained_models[name] = model
    print(f"✅ Accuracy: {accuracy:.2%}")

# Create voting classifier
print("\n🗳️  Creating ensemble voting classifier...")
voting_clf = VotingClassifier(
    estimators=[
        ('lr', trained_models['Logistic Regression']),
        ('rf', trained_models['Random Forest']),
        ('dt', trained_models['Decision Tree']),
        ('knn', trained_models['KNN']),
        ('nb', trained_models['Naive Bayes']),
        ('svc', trained_models['SVC'])
    ],
    voting='soft'
)

voting_clf.fit(X_train_pca, y_train)
voting_accuracy = voting_clf.score(X_test_pca, y_test)
print(f"✅ Voting Classifier Accuracy: {voting_accuracy:.2%}")

# Save models
print("\n💾 Saving models...")
output_dir = "Heart-Disease-Prediction-System/trained_models"
os.makedirs(output_dir, exist_ok=True)

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
    'input_features': 3060,
    'pca_components': n_components,
    'explained_variance': float(pca.explained_variance_ratio_.sum()),
    'voting_accuracy': float(voting_accuracy),
    'individual_accuracies': {k: float(v) for k, v in accuracies.items()},
    'sklearn_version': '1.5.2',
    'n_classes': 4,
    'class_mapping': {
        '0': 'Abnormal Heartbeat (AHB)',
        '1': 'Myocardial Infarction (MI)',
        '2': 'Normal',
        '3': 'History of MI (PM)'
    }
}

info_path = os.path.join(output_dir, "ecg_model_info.txt")
with open(info_path, 'w') as f:
    f.write("ECG Model Information\n")
    f.write("=" * 60 + "\n\n")
    for key, value in model_info.items():
        f.write(f"{key}: {value}\n")

print(f"✅ Saved model info: {info_path}")

print("\n" + "=" * 60)
print("✅ ECG Models Successfully Retrained!")
print("=" * 60)
print(f"\nBest Individual Model: {max(accuracies, key=accuracies.get)} ({max(accuracies.values()):.2%})")
print(f"Ensemble Accuracy: {voting_accuracy:.2%}")
print(f"\nInput: 3060 features (12 leads × 255 points)")
print(f"PCA: {n_components} components ({pca.explained_variance_ratio_.sum():.2%} variance)")
print("\nModels are now compatible with scikit-learn 1.5.2")
print("You can now use the ECG prediction feature!")
