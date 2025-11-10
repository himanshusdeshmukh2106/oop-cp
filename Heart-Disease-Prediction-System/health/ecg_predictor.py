"""
ECG-based Heart Disease Prediction Module
Adapted for Django from: https://github.com/rameshavinash94/Cardiovascular-Detection-using-ECG-images
"""

from skimage.io import imread
from skimage import color
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Django
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, gaussian
from skimage.transform import resize
from skimage import measure
import joblib
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
from natsort import natsorted
from pathlib import Path
import tempfile
import shutil

class ECGPredictor:
    """
    ECG Image Analysis and Heart Disease Prediction
    
    Processes 12-lead ECG images to detect:
    - Normal heart
    - Myocardial Infarction (Heart Attack)
    - Abnormal Heartbeat (Arrhythmia)
    - History of Myocardial Infarction
    """
    
    def __init__(self):
        """Initialize with model paths"""
        self.base_dir = Path(__file__).resolve().parent.parent
        self.models_dir = self.base_dir / 'trained_models'
        self.temp_dir = None
        
    def create_temp_workspace(self):
        """Create temporary directory for processing"""
        self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir
    
    def cleanup_temp_workspace(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def get_image(self, image_path):
        """
        Load ECG image from file path
        Args:
            image_path: Path to ECG image file
        Returns:
            numpy array of image (RGB format)
        """
        image = imread(image_path)
        
        # Handle different image formats
        if len(image.shape) == 2:
            # Grayscale (2D) - convert to RGB (3D)
            image = np.stack([image, image, image], axis=-1)
        elif len(image.shape) == 3:
            # Check number of channels
            if image.shape[2] == 4:
                # RGBA (4 channels) - convert to RGB (3 channels)
                # Remove alpha channel
                image = image[:, :, :3]
            elif image.shape[2] == 2:
                # 2 channels (grayscale + alpha) - use first channel and convert to RGB
                image = np.stack([image[:, :, 0], image[:, :, 0], image[:, :, 0]], axis=-1)
            elif image.shape[2] == 1:
                # Single channel - convert to RGB
                image = np.concatenate([image, image, image], axis=-1)
            # If already 3 channels (RGB), keep as is
        
        return image
    
    def gray_image(self, image):
        """
        Convert image to grayscale and resize
        Args:
            image: RGB, RGBA, or grayscale image array
        Returns:
            Grayscale image resized to standard dimensions
        """
        # Check if already grayscale
        if len(image.shape) == 2:
            image_gray = image
        else:
            # Handle different channel formats
            if image.shape[2] == 4:
                # RGBA (4 channels) - remove alpha channel first
                image = image[:, :, :3]
            elif image.shape[2] == 2:
                # 2 channels (grayscale + alpha) - use first channel only
                image = np.stack([image[:, :, 0], image[:, :, 0], image[:, :, 0]], axis=-1)
            elif image.shape[2] == 1:
                # Single channel - convert to RGB
                image = np.concatenate([image, image, image], axis=-1)
            # Convert to grayscale
            image_gray = color.rgb2gray(image)
        
        image_gray = resize(image_gray, (1572, 2213))
        return image_gray
    
    def divide_leads(self, image):
        """
        Divide ECG image into 13 separate leads
        
        Leads 1-12: Standard 12-lead ECG
        Lead 13: Long rhythm strip
        
        Args:
            image: Grayscale ECG image
        Returns:
            List of 13 lead images
        """
        Lead_1 = image[300:600, 150:643]
        Lead_2 = image[300:600, 646:1135]
        Lead_3 = image[300:600, 1140:1625]
        Lead_4 = image[300:600, 1630:2125]
        Lead_5 = image[600:900, 150:643]
        Lead_6 = image[600:900, 646:1135]
        Lead_7 = image[600:900, 1140:1625]
        Lead_8 = image[600:900, 1630:2125]
        Lead_9 = image[900:1200, 150:643]
        Lead_10 = image[900:1200, 646:1135]
        Lead_11 = image[900:1200, 1140:1625]
        Lead_12 = image[900:1200, 1630:2125]
        Lead_13 = image[1250:1480, 150:2125]
        
        Leads = [Lead_1, Lead_2, Lead_3, Lead_4, Lead_5, Lead_6, 
                 Lead_7, Lead_8, Lead_9, Lead_10, Lead_11, Lead_12, Lead_13]
        
        return Leads
    
    def signal_extraction_scaling(self, Leads):
        """
        Extract ECG signal from each lead using contour detection
        and convert to 1D normalized signal
        
        Args:
            Leads: List of lead images
        Returns:
            None (saves CSV files to temp directory)
        """
        # Change to temp directory for CSV output
        original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            for x, y in enumerate(Leads[:len(Leads)-1]):  # Process first 12 leads
                # Convert to grayscale if needed
                if len(y.shape) == 2:
                    grayscale = y  # Already grayscale
                else:
                    # Handle different channel formats
                    if y.shape[2] == 4:
                        # RGBA (4 channels) - remove alpha channel
                        y = y[:, :, :3]
                    elif y.shape[2] == 2:
                        # 2 channels (grayscale + alpha) - use first channel only
                        y = np.stack([y[:, :, 0], y[:, :, 0], y[:, :, 0]], axis=-1)
                    elif y.shape[2] == 1:
                        # Single channel - convert to RGB
                        y = np.concatenate([y, y, y], axis=-1)
                    grayscale = color.rgb2gray(y)
                
                # Apply gaussian smoothing
                blurred_image = gaussian(grayscale, sigma=0.7)
                # Threshold to separate signal from background
                global_thresh = threshold_otsu(blurred_image)
                binary_global = blurred_image < global_thresh
                # Resize
                binary_global = resize(binary_global, (300, 450))
                
                # Find contours (ECG waveform)
                contours = measure.find_contours(binary_global, 0.8)
                contours_shape = sorted([c.shape for c in contours])[::-1][0:1]
                
                # Extract largest contour (the signal)
                for contour in contours:
                    if contour.shape in contours_shape:
                        test = resize(contour, (255, 2))
                
                # Normalize and scale
                lead_no = x
                scaler = MinMaxScaler()
                fit_transform_data = scaler.fit_transform(test)
                Normalized_Scaled = pd.DataFrame(fit_transform_data[:, 0], columns=['X'])
                Normalized_Scaled = Normalized_Scaled.T
                
                # Save to CSV
                csv_filename = f'Scaled_1DLead_{lead_no+1}.csv'
                Normalized_Scaled.to_csv(csv_filename, index=False)
        
        finally:
            # Return to original directory
            os.chdir(original_dir)
    
    def combine_convert_1d_signal(self):
        """
        Combine all 12 lead signals into single dataframe
        
        Returns:
            DataFrame with combined 1D signals (3060 features)
        """
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            # Read first lead
            test_final = pd.read_csv('Scaled_1DLead_1.csv')
            
            # Combine remaining leads
            for files in natsorted(os.listdir('.')):
                if files.endswith(".csv") and files != 'Scaled_1DLead_1.csv':
                    df = pd.read_csv(files)
                    test_final = pd.concat([test_final, df], axis=1, ignore_index=True)
            
            return test_final
        
        finally:
            os.chdir(original_dir)
    
    def dimensional_reduction(self, test_final):
        """
        Apply standardization and PCA to reduce dimensionality
        
        Args:
            test_final: DataFrame with 3060 features
        Returns:
            DataFrame with reduced dimensions
        """
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        
        # Load scaler if exists
        scaler_path = self.models_dir / 'scaler_ECG.pkl'
        if scaler_path.exists():
            scaler = joblib.load(scaler_path)
            test_scaled = scaler.transform(test_final)
        else:
            test_scaled = test_final
        
        # Load and apply PCA
        pca_model_path = self.models_dir / 'PCA_ECG (1).pkl'
        pca_loaded_model = joblib.load(pca_model_path)
        result = pca_loaded_model.transform(test_scaled)
        final_df = pd.DataFrame(result)
        return final_df
    
    def model_load_predict(self, final_df):
        """
        Load pre-trained model and make prediction
        
        Args:
            final_df: DataFrame with PCA-reduced features
        Returns:
            tuple: (prediction_code, prediction_text, confidence)
        """
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        
        try:
            model_path = self.models_dir / 'Heart_Disease_Prediction_using_ECG (4).pkl'
            
            # Try loading with sklearn compatibility
            import sklearn
            loaded_model = joblib.load(model_path)
            result = loaded_model.predict(final_df)
            
            # Get prediction probabilities if available
            try:
                proba = loaded_model.predict_proba(final_df)
                confidence = float(np.max(proba) * 100)
            except:
                confidence = None
            
            # Map prediction to text
            prediction_map = {
                0: ("Abnormal Heartbeat", "Your ECG shows signs of abnormal heartbeat (arrhythmia). Please consult a cardiologist."),
                1: ("Myocardial Infarction", "Your ECG indicates Myocardial Infarction (heart attack). Seek immediate medical attention!"),
                2: ("Normal", "Your ECG appears normal. Your heart rhythm is healthy."),
                3: ("History of MI", "Your ECG shows signs of previous Myocardial Infarction. Follow up with your cardiologist.")
            }
            
            pred_code = int(result[0])
            pred_label, pred_message = prediction_map.get(pred_code, ("Unknown", "Unable to classify ECG"))
            
            return pred_code, pred_label, pred_message, confidence
            
        except Exception as e:
            # If model loading fails due to version incompatibility
            error_msg = str(e)
            if 'dtype' in error_msg or 'incompatible' in error_msg.lower():
                raise Exception(
                    "ECG model incompatibility detected. The pre-trained models were created with an older "
                    "version of scikit-learn. Please retrain the models or use compatible versions. "
                    "For now, the ECG analysis feature is temporarily unavailable."
                )
            else:
                raise
    
    def predict_from_ecg_image(self, image_path):
        """
        Complete pipeline: Process ECG image and return prediction
        
        Args:
            image_path: Path to uploaded ECG image
        Returns:
            dict with prediction results
        """
        try:
            # Create temp workspace
            self.create_temp_workspace()
            
            # Step 1: Load image
            ecg_image = self.get_image(image_path)
            
            # Step 2: Convert to grayscale
            gray_image = self.gray_image(ecg_image)
            
            # Step 3: Divide into leads
            leads = self.divide_leads(gray_image)
            
            # Step 4: Extract and scale signals
            self.signal_extraction_scaling(leads)
            
            # Step 5: Combine signals
            combined_signal = self.combine_convert_1d_signal()
            
            # Step 6: Apply PCA
            reduced_features = self.dimensional_reduction(combined_signal)
            
            # Step 7: Predict
            pred_code, pred_label, pred_message, confidence = self.model_load_predict(reduced_features)
            
            result = {
                'success': True,
                'prediction_code': pred_code,
                'prediction_label': pred_label,
                'prediction_message': pred_message,
                'confidence': confidence,
                'num_features': combined_signal.shape[1],
                'reduced_features': reduced_features.shape[1]
            }
            
            return result
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'prediction_label': 'Error',
                'prediction_message': f'Failed to process ECG image: {str(e)}'
            }
        
        finally:
            # Clean up temp files
            self.cleanup_temp_workspace()
