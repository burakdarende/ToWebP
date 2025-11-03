"""
Quick test script to verify the converter works
"""
from converter import ImageToWebPConverter
from PIL import Image
import os

def create_test_images():
    """Create some test images for testing"""
    test_folder = "test_images"
    
    # Create folder structure
    os.makedirs(f"{test_folder}/subfolder1", exist_ok=True)
    os.makedirs(f"{test_folder}/subfolder2/nested", exist_ok=True)
    
    # Create test images
    # Red image
    img1 = Image.new('RGB', (100, 100), color='red')
    img1.save(f"{test_folder}/red.jpg")
    
    # Green image with transparency
    img2 = Image.new('RGBA', (100, 100), color='green')
    img2.save(f"{test_folder}/subfolder1/green.png")
    
    # Blue image
    img3 = Image.new('RGB', (100, 100), color='blue')
    img3.save(f"{test_folder}/subfolder2/blue.bmp")
    
    # Yellow image in nested folder
    img4 = Image.new('RGB', (100, 100), color='yellow')
    img4.save(f"{test_folder}/subfolder2/nested/yellow.jpg")
    
    print(f"✅ Test images created in '{test_folder}' folder")
    print(f"   - {test_folder}/red.jpg")
    print(f"   - {test_folder}/subfolder1/green.png")
    print(f"   - {test_folder}/subfolder2/blue.bmp")
    print(f"   - {test_folder}/subfolder2/nested/yellow.jpg")
    return test_folder

def test_conversion():
    """Test the conversion"""
    print("\n" + "="*60)
    print("TESTING IMAGE TO WEBP CONVERTER")
    print("="*60 + "\n")
    
    # Create test images
    test_folder = create_test_images()
    
    print("\n" + "-"*60)
    print("Starting conversion...")
    print("-"*60 + "\n")
    
    # Create converter
    converter = ImageToWebPConverter(quality=85, lossless=False, method=4)
    
    # Convert
    def progress(msg, current, total):
        print(f"[{current}/{total}] {msg}")
    
    output_folder, total, processed, errors = converter.convert_folder(
        test_folder,
        progress_callback=progress
    )
    
    print("\n" + "="*60)
    print("CONVERSION COMPLETE!")
    print("="*60)
    print(f"📂 Output folder: {output_folder}")
    print(f"📊 Total images: {total}")
    print(f"✅ Successfully converted: {processed}")
    print(f"❌ Errors: {len(errors)}")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
    
    print("\n✨ Test completed successfully!")
    print(f"Check the '{output_folder}' folder to see the results.\n")

if __name__ == "__main__":
    test_conversion()
