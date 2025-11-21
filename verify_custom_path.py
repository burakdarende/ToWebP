import os
import shutil
from pathlib import Path
from converter import ImageToWebPConverter
from PIL import Image

def test_custom_output_path():
    print("🧪 Testing Custom Output Path Feature...")
    
    # Setup test environment
    test_dir = Path("test_env")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    source_dir = test_dir / "source"
    source_dir.mkdir()
    
    output_dir_custom = test_dir / "custom_output"
    output_dir_custom.mkdir()
    
    # Create dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_path = source_dir / "test_image.jpg"
    img.save(img_path)
    
    converter = ImageToWebPConverter()
    
    # Test 1: Single File Conversion with Custom Output
    print("\n[1] Testing Single File Conversion with Custom Output...")
    output_file, _, _, _ = converter.convert_single_file(
        str(img_path),
        output_folder=str(output_dir_custom)
    )
    
    if Path(output_file).parent == output_dir_custom and Path(output_file).exists():
        print("✅ Success: File converted to custom output folder.")
    else:
        print(f"❌ Failure: File not found in custom output folder. Output: {output_file}")
        
    # Test 2: Folder Conversion with Custom Output
    print("\n[2] Testing Folder Conversion with Custom Output...")
    # Clear output
    for item in output_dir_custom.iterdir():
        if item.is_file():
            item.unlink()
            
    output_folder_res, _, _, _ = converter.convert_folder(
        str(source_dir),
        output_folder=str(output_dir_custom)
    )
    
    if Path(output_folder_res) == output_dir_custom:
        # Check if file exists inside
        expected_file = output_dir_custom / "test_image.webp"
        if expected_file.exists():
             print("✅ Success: Folder converted to custom output folder.")
        else:
             print(f"❌ Failure: File not found in custom output folder.")
    else:
        print(f"❌ Failure: Output folder path mismatch. Got: {output_folder_res}, Expected: {output_dir_custom}")

    # Test 3: Default Behavior (No custom output)
    print("\n[3] Testing Default Behavior...")
    output_file_default, _, _, _ = converter.convert_single_file(str(img_path))
    if Path(output_file_default).parent == source_dir:
        print("✅ Success: File converted to source folder (default).")
    else:
        print(f"❌ Failure: Default behavior incorrect. Output: {output_file_default}")

    # Cleanup
    try:
        shutil.rmtree(test_dir)
        print("\n🧹 Cleanup done.")
    except:
        pass

if __name__ == "__main__":
    test_custom_output_path()
