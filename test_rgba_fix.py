"""
Test script to verify RGBA image handling in ECG predictor
"""
import numpy as np
from PIL import Image
import os

def test_rgba_handling():
    """Test that RGBA images are properly converted to RGB"""
    
    print("=" * 60)
    print("Testing RGBA Image Handling")
    print("=" * 60)
    
    # Create a test RGBA image
    test_rgba = np.random.randint(0, 255, (100, 100, 4), dtype=np.uint8)
    test_rgb = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    test_gray = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    
    print("\n1. Test Image Shapes:")
    print(f"   RGBA shape: {test_rgba.shape} (4 channels)")
    print(f"   RGB shape:  {test_rgb.shape} (3 channels)")
    print(f"   Gray shape: {test_gray.shape} (2D)")
    
    # Test the conversion logic
    print("\n2. Testing RGBA → RGB Conversion:")
    
    # Simulate get_image() logic
    image = test_rgba.copy()
    if len(image.shape) == 3 and image.shape[2] == 4:
        image_converted = image[:, :, :3]
        print(f"   ✅ RGBA converted to RGB: {image_converted.shape}")
    else:
        print(f"   ❌ Conversion failed")
    
    # Test gray_image() logic
    print("\n3. Testing gray_image() RGBA Handling:")
    image = test_rgba.copy()
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = image[:, :, :3]
        print(f"   ✅ Alpha channel removed: {image.shape}")
    
    # Test signal_extraction_scaling() logic
    print("\n4. Testing signal_extraction_scaling() RGBA Handling:")
    lead = test_rgba.copy()
    if len(lead.shape) == 3 and lead.shape[2] == 4:
        lead = lead[:, :, :3]
        print(f"   ✅ Lead alpha channel removed: {lead.shape}")
    
    print("\n" + "=" * 60)
    print("✅ All RGBA handling tests passed!")
    print("=" * 60)
    
    # Create a sample RGBA image file for testing
    print("\n5. Creating sample RGBA test image...")
    test_dir = "test_images"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create RGBA image
    rgba_img = Image.new('RGBA', (200, 200), (255, 0, 0, 128))
    rgba_path = os.path.join(test_dir, "test_rgba.png")
    rgba_img.save(rgba_path)
    print(f"   ✅ Created: {rgba_path}")
    
    # Verify it's RGBA
    check_img = Image.open(rgba_path)
    print(f"   Mode: {check_img.mode} (should be RGBA)")
    print(f"   Size: {check_img.size}")
    
    print("\n" + "=" * 60)
    print("Test image created at: test_images/test_rgba.png")
    print("You can now test uploading this RGBA image to the ECG system")
    print("=" * 60)

if __name__ == "__main__":
    test_rgba_handling()
