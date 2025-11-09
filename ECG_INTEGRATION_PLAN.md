# ECG-Based Heart Disease Detection - Integration Plan

## Overview
The ECG system analyzes **ECG images** (not numerical data) to detect cardiovascular diseases using image processing and machine learning.

## How the ECG System Works

### 1. **Input**: ECG Image Upload
- User uploads a 12-lead ECG image (paper ECG scan)
- Image format: Standard ECG printout with grid lines

### 2. **Image Processing Pipeline**

#### Step 1: Grayscale Conversion
- Convert RGB image to grayscale
- Resize to standard dimensions (1572x2213)

#### Step 2: Lead Division
- Divide ECG image into **13 leads**:
  - **Leads 1-3**: Bipolar limb leads
  - **Leads 4-6**: Augmented unipolar limb leads (aVR, aVL, aVF)
  - **Leads 7-12**: Unipolar chest leads (V1-V6)
  - **Lead 13**: Long lead (rhythm strip)

#### Step 3: Preprocessing Each Lead
- Apply Gaussian filter (smoothing)
- Otsu thresholding (separate signal from background/grid)
- Resize to 300x450 pixels
- Remove grid lines, keep only ECG waveform

#### Step 4: Signal Extraction
- Use **contour detection** to extract the ECG waveform
- Find the largest contour (the actual signal)
- Convert 2D image signal to 1D array (255 points)

#### Step 5: Normalization & Scaling
- Apply MinMaxScaler to normalize signal values
- Save each lead as CSV (255 data points per lead)

#### Step 6: Combine All Leads
- Concatenate all 12 leads into single dataset
- Total: 12 leads × 255 points = 3,060 features

#### Step 7: Dimensionality Reduction
- Apply **PCA (Principal Component Analysis)**
- Reduce 3,060 features to manageable size
- Uses pre-trained PCA model (`PCA_ECG.pkl`)

#### Step 8: Classification
- Feed reduced features to ML model
- Uses pre-trained classifier (`Heart_Disease_Prediction_using_ECG.pkl`)
- Predicts one of 4 categories

### 3. **Output**: Disease Classification

The model classifies ECG into **4 categories**:
1. **Normal** - Healthy heart
2. **Myocardial Infarction (MI)** - Heart attack
3. **Abnormal Heartbeat** - Arrhythmia
4. **History of MI** - Previous heart attack

## Technical Stack

### Libraries Used:
- **scikit-image**: Image processing (grayscale, gaussian filter, thresholding, contours)
- **scikit-learn**: ML models, PCA, MinMaxScaler
- **pandas**: Data manipulation
- **matplotlib**: Visualization
- **joblib**: Model serialization
- **streamlit**: Web interface

### Pre-trained Models:
1. **PCA_ECG.pkl** - Dimensionality reduction model
2. **Heart_Disease_Prediction_using_ECG.pkl** - Classification model

## Dataset Information

**Source**: https://data.mendeley.com/datasets/gwbz3fsgp8/2

**Categories**:
- Normal Person ECG: 284 patients × 12 leads = 3,408 images
- Myocardial Infarction: 240 patients × 12 leads = 2,880 images
- Abnormal Heartbeat: 233 patients × 12 leads = 2,796 images
- History of MI: 172 patients × 12 leads = 2,064 images

**Total**: 11,148 ECG images

## Integration Strategy for Our Project

### Option 1: Separate ECG Predictor Module
Create a new prediction option in the Django app:
- **Current**: Numerical data input (age, BP, cholesterol, etc.)
- **New**: ECG image upload option
- User can choose between two prediction methods

### Option 2: Combined Prediction
- Use both methods together for more accurate diagnosis
- Numerical data + ECG image = comprehensive analysis

### Implementation Steps:

1. **Add ECG Module to Django**
   - Create `ecg_predictor.py` in `health/` directory
   - Port the ECG class from the cloned repo
   - Add image upload field to Patient model

2. **Update Views**
   - Add new view for ECG upload
   - Process image through ECG pipeline
   - Return classification result

3. **Update Templates**
   - Add ECG upload form to patient dashboard
   - Show processing steps (optional)
   - Display result with visualization

4. **Add Dependencies**
   - scikit-image
   - natsort
   - Update requirements.txt

5. **Copy Pre-trained Models**
   - Copy `PCA_ECG.pkl` and `Heart_Disease_Prediction_using_ECG.pkl`
   - Place in `trained_models/` directory

6. **Create New Template**
   - `ecg_upload.html` - Upload interface
   - `ecg_result.html` - Show classification result

## Benefits of Integration

1. **Dual Prediction Methods**
   - Numerical data: Quick screening
   - ECG image: Detailed analysis

2. **More Accurate Diagnosis**
   - Combines clinical data with ECG analysis
   - Better detection of specific conditions

3. **Professional Tool**
   - Doctors can upload patient ECG scans
   - Automated analysis saves time

4. **Educational Value**
   - Shows complete workflow
   - Visualizes image processing steps

## Challenges to Address

1. **Large Image Files**
   - ECG images can be large
   - Need efficient storage/processing

2. **Model Size**
   - Pre-trained models need to be included
   - May increase deployment size

3. **Processing Time**
   - Image processing takes longer than numerical prediction
   - Need loading indicators

4. **Image Quality**
   - Requires good quality ECG scans
   - Need validation for image format/quality

## Next Steps

1. Review the ECG code and adapt for Django
2. Create database schema for ECG images
3. Implement image upload functionality
4. Test with sample ECG images
5. Integrate with existing prediction system
6. Update UI/UX for dual prediction modes

---

**Current System**: Numerical data → 5 ML algorithms → Binary prediction (0/1)

**ECG System**: ECG image → Image processing → PCA → ML classifier → 4-class prediction

**Integrated System**: Both methods available for comprehensive heart disease detection
