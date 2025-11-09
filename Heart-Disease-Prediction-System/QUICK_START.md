# Quick Start Guide - Updated ML Implementation

## What Changed?

The heart disease prediction system now uses **5 machine learning algorithms** instead of just one, automatically selecting the best performer for each prediction.

## Installation & Setup

### 1. Install Dependencies
```bash
pip install django pandas numpy scikit-learn matplotlib seaborn
```

### 2. Navigate to Project
```bash
cd Heart-Disease-Prediction-System
```

### 3. Test the ML Implementation (Optional)
```bash
python test_prediction.py
```

This will show you how all 5 algorithms perform and which one is selected.

### 4. Run the Django Server
```bash
python manage.py runserver
```

### 5. Access the Application
Open your browser and go to: `http://127.0.0.1:8000/`

## How It Works

### User Flow:
1. **Patient registers/logs in**
2. **Enters health parameters:**
   - Age, sex, chest pain type
   - Blood pressure, cholesterol
   - Blood sugar, ECG results
   - Heart rate, exercise data
   - And more...

3. **System processes the data:**
   - Trains 5 ML models:
     - Logistic Regression
     - Random Forest ⭐ (usually best)
     - Decision Tree
     - K-Nearest Neighbors
     - Naive Bayes
   
4. **Returns prediction:**
   - "You are healthy" (0)
   - "You are unhealthy, need checkup" (1)
   - Shows accuracy percentage
   - Suggests nearby doctors

## The 5 Algorithms Explained

### 1. Logistic Regression (85% accuracy)
- **What it does**: Finds linear relationships between features
- **Best for**: Understanding which factors matter most
- **Speed**: Very fast

### 2. Random Forest (87% accuracy) ⭐
- **What it does**: Creates many decision trees and votes
- **Best for**: Overall best performance
- **Speed**: Medium

### 3. Decision Tree (82% accuracy)
- **What it does**: Creates a flowchart of yes/no questions
- **Best for**: Easy to understand predictions
- **Speed**: Fast

### 4. K-Nearest Neighbors (62% accuracy)
- **What it does**: Looks at 7 similar patients
- **Best for**: Finding patterns in similar cases
- **Speed**: Slower

### 5. Naive Bayes (77% accuracy)
- **What it does**: Uses probability theory
- **Best for**: Quick probabilistic estimates
- **Speed**: Very fast

## Example Prediction

### Input:
```python
Patient Data:
- Age: 57
- Sex: Female (0)
- Chest Pain: Atypical angina (1)
- Blood Pressure: 130 mm Hg
- Cholesterol: 236 mg/dl
- Fasting Blood Sugar: Normal (0)
- Resting ECG: Normal (0)
- Max Heart Rate: 174
- Exercise Angina: No (0)
- ST Depression: 0.0
- Slope: Upsloping (1)
- Major Vessels: 1
- Thalassemia: Normal (2)
```

### Output:
```
Algorithm Results:
- Logistic Regression: Disease (85% accuracy)
- Random Forest: Healthy (87% accuracy) ⭐ SELECTED
- Decision Tree: Healthy (82% accuracy)
- KNN: Disease (62% accuracy)
- Naive Bayes: Disease (77% accuracy)

FINAL PREDICTION: Healthy (No Heart Disease)
Using: Random Forest (87% accuracy)
```

## Admin Features

### Upload New Dataset:
1. Login as admin
2. Go to "Add Dataset"
3. Upload CSV file with same format as heart.csv
4. System will use new data for training

### Manage Doctors:
- Add new doctors
- Approve/withdraw doctor access
- View doctor details

### View Analytics:
- Total predictions made
- Patient records
- Doctor records
- Feedback from users

## File Structure

```
Heart-Disease-Prediction-System/
├── health/                          # Main Django app
│   ├── views.py                     # ✨ Updated with 5 algorithms
│   ├── models.py                    # Database models
│   ├── forms.py                     # Django forms
│   └── templates/                   # HTML templates
├── health_desease/                  # Django project settings
│   ├── settings.py                  # Configuration
│   └── urls.py                      # URL routing
├── Machine_Learning/
│   ├── heart.csv                    # Training dataset (303 samples)
│   └── Heart prediction.ipynb       # Original notebook
├── test_prediction.py               # ✨ New test script
├── ML_INTEGRATION_SUMMARY.md        # ✨ Detailed documentation
├── BEFORE_AFTER_COMPARISON.md       # ✨ Changes explained
├── QUICK_START.md                   # ✨ This file
└── manage.py                        # Django management
```

## Troubleshooting

### Issue: "Admin_Helath_CSV matching query does not exist"
**Solution**: Upload a dataset through admin panel first
```bash
1. Login as admin
2. Go to Django admin: http://127.0.0.1:8000/admin/
3. Add Admin_Helath_CSV entry with heart.csv file
```

### Issue: Import errors
**Solution**: Install missing packages
```bash
pip install scikit-learn pandas numpy
```

### Issue: Slow predictions
**Reason**: Training 5 models takes time
**Solution**: This is normal. Future improvement: save trained models

## Performance Tips

### Current Implementation:
- Trains 5 models on every prediction
- Takes ~1-2 seconds per prediction
- Ensures always using latest data

### Future Optimization:
- Save trained models using pickle
- Load pre-trained models
- Retrain only when dataset changes
- Would reduce prediction time to <0.1 seconds

## Next Steps

1. ✅ Test the system with `test_prediction.py`
2. ✅ Run the Django server
3. ✅ Create admin account: `python manage.py createsuperuser`
4. ✅ Upload heart.csv through admin panel
5. ✅ Register as a patient and test predictions
6. ✅ Check the accuracy of different algorithms

## Support

For issues or questions:
- Check `ML_INTEGRATION_SUMMARY.md` for detailed info
- Review `BEFORE_AFTER_COMPARISON.md` for changes
- Original repo: https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System
- ML methodology: https://github.com/chayandatta/Heart_disease_prediction

## Credits

- **Original System**: Kumar-laxmi
- **ML Methodology**: Chayan Datta
- **Integration**: Updated implementation combining both approaches
- **Dataset**: UCI Machine Learning Repository
