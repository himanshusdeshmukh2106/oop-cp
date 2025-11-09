"""
Retrain ECG models with current scikit-learn version
This script retrains the ECG prediction models to be compatible with scikit-learn 1.5.2
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import joblib
import os

print("=" * 60)
print("ECG Model Retraining Script")
print("=" * 60)

# Check if dataset exists
dataset_path = "Cardiovascular-Detection-using-ECG-images/Final_Dataset/With_dimensionality_reduction"

if not os.path.exists(dataset_path):
    print(f"\n❌ Error: Dataset not found at {dataset_path}")
    print("Please ensure the ECG dataset is available.")
    exit(1)

# Load the dataset
print("\n📂 Loading ECG dataset...")
try:
    # Try to find CSV files in the dataset directory
    csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found in dataset directory")
        exit(1)
    
    print(f"Found {len(csv_files)} CSV file(s)")
    
    # Load the first CSV file (or combine if multiple)
    df = pd.read_csv(os.path.join(dataset_path, csv_files[0]))
    print(f"✅ Loaded dataset with shape: {df.shape}")
    
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    exit(1)

# Prepare data
print("\n🔧 Preparing data...")
X = df.iloc[:, :-1]  # All columns except last
y = df.iloc[:, -1]   # Last column is target

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Classes: {np.unique(y)}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Apply PCA
print("\n🔬 Applying PCA for dimensionality reduction...")
n_components = min(50, X_train.shape[1])  # Use 50 components or less
pca = PCA(n_components=n_components, random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

print(f"✅ Reduced to {n_components} components")
print(f"Explained variance: {pca.explained_variance_ratio_.sum():.2%}")

# Train models
print("\n🤖 Training classification models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
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
    'pca_components': n_components,
    'explained_variance': float(pca.explained_variance_ratio_.sum()),
    'voting_accuracy': float(voting_accuracy),
    'individual_accuracies': {k: float(v) for k, v in accuracies.items()},
    'sklearn_version': '1.5.2',
    'n_classes': len(np.unique(y)),
    'classes': list(np.unique(y))
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
print("\nModels are now compatible with scikit-learn 1.5.2")
print("You can now use the ECG prediction feature!")
