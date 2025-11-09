# Dataset Information

## Which Dataset is Being Used?

The system uses the **UCI Heart Disease Dataset** stored at:
```
Heart-Disease-Prediction-System/Machine_Learning/heart.csv
```

---

## Dataset Overview

### Basic Statistics
- **Total Samples**: 303 patients
- **Features**: 13 medical parameters
- **Target**: Binary classification (0 = Healthy, 1 = Disease)
- **Source**: UCI Machine Learning Repository

### Class Distribution
- **Healthy (0)**: 138 patients (45.5%)
- **Disease (1)**: 165 patients (54.5%)
- **Balance**: Relatively balanced dataset

---

## The 13 Features

| # | Feature | Description | Type | Range |
|---|---------|-------------|------|-------|
| 1 | **age** | Age in years | Numeric | 29-77 |
| 2 | **sex** | Sex | Binary | 0=Female, 1=Male |
| 3 | **cp** | Chest pain type | Categorical | 0-3 |
| 4 | **trestbps** | Resting blood pressure (mm Hg) | Numeric | 94-200 |
| 5 | **chol** | Serum cholesterol (mg/dl) | Numeric | 126-564 |
| 6 | **fbs** | Fasting blood sugar > 120 mg/dl | Binary | 0=False, 1=True |
| 7 | **restecg** | Resting ECG results | Categorical | 0-2 |
| 8 | **thalach** | Maximum heart rate achieved | Numeric | 71-202 |
| 9 | **exang** | Exercise induced angina | Binary | 0=No, 1=Yes |
| 10 | **oldpeak** | ST depression induced by exercise | Numeric | 0.0-6.2 |
| 11 | **slope** | Slope of peak exercise ST segment | Categorical | 0-2 |
| 12 | **ca** | Number of major vessels (0-3) colored by fluoroscopy | Numeric | 0-4 |
| 13 | **thal** | Thalassemia | Categorical | 0-3 |

### Target Variable
- **target**: 0 = No heart disease, 1 = Heart disease present

---

## Feature Details

### 1. Age (age)
- **Range**: 29 to 77 years
- **Mean**: ~54 years
- **Type**: Continuous numeric

### 2. Sex (sex)
- **0**: Female (31.7%)
- **1**: Male (68.3%)
- **Note**: Males are more represented in this dataset

### 3. Chest Pain Type (cp)
- **0**: Typical angina
- **1**: Atypical angina
- **2**: Non-anginal pain
- **3**: Asymptomatic

### 4. Resting Blood Pressure (trestbps)
- **Range**: 94-200 mm Hg
- **Mean**: ~132 mm Hg
- **Normal**: <120 mm Hg

### 5. Serum Cholesterol (chol)
- **Range**: 126-564 mg/dl
- **Mean**: ~246 mg/dl
- **Normal**: <200 mg/dl
- **Borderline high**: 200-239 mg/dl
- **High**: ≥240 mg/dl

### 6. Fasting Blood Sugar (fbs)
- **0**: ≤120 mg/dl (85.1%)
- **1**: >120 mg/dl (14.9%)

### 7. Resting ECG (restecg)
- **0**: Normal
- **1**: ST-T wave abnormality
- **2**: Left ventricular hypertrophy

### 8. Maximum Heart Rate (thalach)
- **Range**: 71-202 bpm
- **Mean**: ~150 bpm
- **Higher is generally better**

### 9. Exercise Induced Angina (exang)
- **0**: No (67.3%)
- **1**: Yes (32.7%)

### 10. ST Depression (oldpeak)
- **Range**: 0.0-6.2
- **Mean**: ~1.04
- **Lower is better**

### 11. Slope of ST Segment (slope)
- **0**: Downsloping (worse)
- **1**: Flat
- **2**: Upsloping (better)

### 12. Major Vessels (ca)
- **Range**: 0-4 vessels
- **Mean**: ~0.73
- **Fewer is better**

### 13. Thalassemia (thal)
- **0**: Unknown
- **1**: Normal
- **2**: Fixed defect
- **3**: Reversible defect

---

## Dataset Origin

### Source
**UCI Machine Learning Repository - Heart Disease Dataset**

### Original Creators
1. **Hungarian Institute of Cardiology**, Budapest: Andras Janosi, M.D.
2. **University Hospital**, Zurich, Switzerland: William Steinbrunn, M.D.
3. **University Hospital**, Basel, Switzerland: Matthias Pfisterer, M.D.
4. **V.A. Medical Center**, Long Beach and Cleveland Clinic Foundation: Robert Detrano, M.D., Ph.D.

### Publication
This is the **Cleveland database** - the most commonly used subset of the UCI Heart Disease dataset.

### Original Dataset
- The original database contains **76 attributes**
- This version uses a subset of **14 attributes** (13 features + 1 target)
- Most published experiments use this 14-attribute subset

---

## How the System Uses This Dataset

### 1. Pre-trained Models (Current Approach)
```python
# Models are trained once using:
python train_and_save_models.py

# This loads: Machine_Learning/heart.csv
# Trains 5 models and saves them to: trained_models/
```

**Training Split:**
- 80% training (242 samples)
- 20% testing (61 samples)
- Stratified split (maintains class balance)
- Random seed: 123 (for reproducibility)

### 2. Django Application (Fallback)
If pre-trained models don't exist, the Django app can:
- Load dataset from database (`Admin_Helath_CSV` model)
- Train models on-the-fly
- Make predictions

**Database Model:**
```python
class Admin_Helath_CSV(models.Model):
    name = models.CharField(max_length=100, null=True)
    csv_file = models.FileField(null=True, blank=True)
```

---

## Dataset Characteristics

### Strengths
✅ **Well-balanced**: 45.5% healthy, 54.5% disease
✅ **Real medical data**: From actual patients
✅ **Standardized**: Widely used in research
✅ **Complete**: No missing values
✅ **Diverse features**: Covers multiple health indicators

### Limitations
⚠️ **Small size**: Only 303 samples
⚠️ **Specific population**: Cleveland Clinic patients (1980s)
⚠️ **Geographic bias**: Primarily from one location
⚠️ **Temporal bias**: Data from 1980s
⚠️ **Gender imbalance**: 68% male, 32% female
⚠️ **Age range**: Limited to 29-77 years

---

## Model Performance on This Dataset

### Test Set Results (61 samples)

| Model | Accuracy | Notes |
|-------|----------|-------|
| **Random Forest** | **86.89%** | Best overall |
| Logistic Regression | 85.25% | Good linear model |
| Decision Tree | 81.97% | Simple rules |
| Naive Bayes | 77.05% | Probabilistic |
| KNN (k=7) | 62.30% | Instance-based |

### Why These Accuracies?
- Dataset is relatively small (303 samples)
- Some cases are genuinely borderline
- Real medical data has inherent uncertainty
- 86.89% is excellent for medical diagnosis

---

## Sample Data

### Example Healthy Patient (target=0)
```
Age: 58, Male
Blood Pressure: 128 mm Hg
Cholesterol: 216 mg/dl
Max Heart Rate: 131 bpm
No exercise angina
ST Depression: 0.0
```

### Example Disease Patient (target=1)
```
Age: 49, Female
Blood Pressure: 130 mm Hg
Cholesterol: 269 mg/dl
Max Heart Rate: 163 bpm
No exercise angina
ST Depression: 0.0
```

**Note**: Even similar-looking patients can have different outcomes based on subtle feature combinations.

---

## Using a Different Dataset

### If You Want to Use Your Own Data:

1. **Format Requirements:**
   - CSV file with same 14 columns
   - Same column names and order
   - Same value ranges and encodings
   - No missing values

2. **Upload via Django Admin:**
   ```
   1. Login as admin
   2. Go to Admin_Helath_CSV
   3. Upload your CSV file
   4. System will use it for training
   ```

3. **Retrain Models:**
   ```bash
   # Update train_and_save_models.py to use new dataset
   # Then run:
   python train_and_save_models.py
   ```

### Important Considerations:
- ⚠️ New data should have similar distribution
- ⚠️ Models may need retuning for different populations
- ⚠️ Validate on appropriate test set
- ⚠️ Consider ethical and privacy implications

---

## Dataset Statistics Summary

```
Total Samples: 303
Features: 13
Target Classes: 2 (Healthy/Disease)

Age: 29-77 years (mean: 54)
Sex: 68% Male, 32% Female
Blood Pressure: 94-200 mm Hg (mean: 132)
Cholesterol: 126-564 mg/dl (mean: 246)
Max Heart Rate: 71-202 bpm (mean: 150)

Class Balance:
  Healthy (0): 138 (45.5%)
  Disease (1): 165 (54.5%)

Train/Test Split:
  Training: 242 samples (80%)
  Testing: 61 samples (20%)
```

---

## References

### Dataset Citation
```
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository
[http://archive.ics.uci.edu/ml]. Irvine, CA: University of California,
School of Information and Computer Science.
```

### Original Research
- Detrano, R., et al. (1989). International application of a new probability
  algorithm for the diagnosis of coronary artery disease. American Journal
  of Cardiology, 64, 304-310.

### Dataset URL
- https://archive.ics.uci.edu/ml/datasets/Heart+Disease

---

## Conclusion

The system uses the **UCI Heart Disease Dataset (Cleveland)** with:
- ✅ 303 real patient records
- ✅ 13 medical features
- ✅ Binary classification (healthy/disease)
- ✅ Well-balanced classes
- ✅ Proven track record in research

This dataset is **ideal for learning and demonstration** but should be supplemented with more recent, diverse data for production medical applications.
