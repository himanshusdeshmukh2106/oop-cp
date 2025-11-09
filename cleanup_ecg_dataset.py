"""
Cleanup ECG dataset - Keep only 30 sample images per category
and remove unnecessary files
"""

import os
import shutil
from pathlib import Path

print("=" * 70)
print("ECG Dataset Cleanup Script")
print("=" * 70)

# Base directory
base_dir = "Cardiovascular-Detection-using-ECG-images"
dataset_dir = os.path.join(base_dir, "ECG_IMAGES_DATASET")

# Categories to keep samples from
categories = [
    'Normal Person ECG Images (284x12=3408)',
    'ECG Images of Myocardial Infarction Patients (240x12=2880)',
    'ECG Images of Patient that have abnormal heartbeat (233x12=2796)',
    'ECG Images of Patient that have History of MI (172x12=2064)'
]

print("\n📂 Step 1: Keeping 30 sample images per category...")

for category in categories:
    category_path = os.path.join(dataset_dir, category)
    
    if not os.path.exists(category_path):
        print(f"⚠️  {category} not found, skipping...")
        continue
    
    # Get all image files
    image_files = [f for f in os.listdir(category_path) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    total_images = len(image_files)
    
    if total_images <= 30:
        print(f"✅ {category}: {total_images} images (keeping all)")
        continue
    
    # Keep first 30, delete the rest
    images_to_delete = image_files[30:]
    
    print(f"🗑️  {category}: Deleting {len(images_to_delete)} images (keeping 30/{total_images})")
    
    for img_file in images_to_delete:
        try:
            os.remove(os.path.join(category_path, img_file))
        except Exception as e:
            print(f"   ⚠️  Error deleting {img_file}: {e}")

print("\n🗑️  Step 2: Removing unnecessary directories...")

# Directories to remove
dirs_to_remove = [
    'preproceed_images',  # 1.6 GB
    'preprocessed_1d',    # 56 MB
    'Combined1d_csv',     # 56 MB
    'Final_Dataset',      # 59 MB
    'video',              # 34 MB
    'docs',               # 2 MB
    'colabs',             # 4 MB
    'img',                # 3 MB
    '.github',
    '.idea'
]

total_removed = 0

for dir_name in dirs_to_remove:
    dir_path = os.path.join(base_dir, dir_name)
    
    if os.path.exists(dir_path):
        try:
            # Get size before deletion
            size = sum(f.stat().st_size for f in Path(dir_path).rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            
            shutil.rmtree(dir_path)
            total_removed += size_mb
            print(f"✅ Removed {dir_name} (~{size_mb:.1f} MB)")
        except Exception as e:
            print(f"⚠️  Error removing {dir_name}: {e}")
    else:
        print(f"⏭️  {dir_name} not found, skipping...")

print("\n🗑️  Step 3: Removing unnecessary files...")

# Files to remove
files_to_remove = [
    'Cardiovascular Diseases Prediction from ECG images.pdf',
    'ppt_Cardiovascular Diseases Prediction from ECG images.pdf',
    'README.md',
    '.DS_Store'
]

for file_name in files_to_remove:
    file_path = os.path.join(base_dir, file_name)
    
    if os.path.exists(file_path):
        try:
            size = os.path.getsize(file_path) / (1024 * 1024)
            os.remove(file_path)
            total_removed += size
            print(f"✅ Removed {file_name} (~{size:.1f} MB)")
        except Exception as e:
            print(f"⚠️  Error removing {file_name}: {e}")

print("\n🗑️  Step 4: Removing old/unused model files...")

# Remove old incompatible models from model_pkl
model_pkl_dir = os.path.join(base_dir, "model_pkl")
if os.path.exists(model_pkl_dir):
    try:
        size = sum(f.stat().st_size for f in Path(model_pkl_dir).rglob('*') if f.is_file())
        size_mb = size / (1024 * 1024)
        shutil.rmtree(model_pkl_dir)
        total_removed += size_mb
        print(f"✅ Removed model_pkl directory (~{size_mb:.1f} MB)")
    except Exception as e:
        print(f"⚠️  Error removing model_pkl: {e}")

print("\n📊 Final Statistics:")
print(f"Total space freed: ~{total_removed:.1f} MB")

# Count remaining images
print("\n📁 Remaining ECG sample images:")
for category in categories:
    category_path = os.path.join(dataset_dir, category)
    if os.path.exists(category_path):
        image_files = [f for f in os.listdir(category_path) 
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"  {category}: {len(image_files)} images")

print("\n" + "=" * 70)
print("✅ Cleanup Complete!")
print("=" * 70)
print("\nWhat's left:")
print("  ✅ 30 sample ECG images per category (120 total)")
print("  ✅ Trained models in Heart-Disease-Prediction-System/trained_models/")
print("  ✅ ECG predictor code")
print("\nRemoved:")
print("  🗑️  Preprocessed images and datasets (~1.8 GB)")
print("  🗑️  Documentation and presentations")
print("  🗑️  Old incompatible models")
print("  🗑️  Unnecessary directories")
print(f"\nTotal saved: ~{total_removed:.1f} MB")

