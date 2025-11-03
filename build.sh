#!/bin/bash
# Build script for macOS/Linux
# Creates standalone executable using PyInstaller

echo "==============================================="
echo "  Image to WebP Converter - Build Script"
echo "==============================================="
echo ""

# Check if PyInstaller is installed
echo "Checking for PyInstaller..."
python3 -c "import PyInstaller" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "PyInstaller not found. Installing..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "Failed to install PyInstaller. Please install manually:"
        echo "  pip3 install pyinstaller"
        exit 1
    fi
fi

echo "PyInstaller found!"
echo ""

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec
echo "Clean complete!"
echo ""

# Build executable
echo "Building executable..."
echo ""

python3 build_exe.py

if [ $? -eq 0 ]; then
    echo ""
    echo "==============================================="
    echo "  BUILD SUCCESSFUL!"
    echo "==============================================="
    echo ""
    echo "Your executable is ready at:"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  $(pwd)/dist/ImageToWebP.app"
        echo ""
        echo "You can now distribute this app without requiring Python!"
        echo ""
        
        # Ask if user wants to run the app
        read -p "Do you want to test the app now? (Y/N) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Starting app..."
            open "./dist/ImageToWebP.app"
        fi
    else
        echo "  $(pwd)/dist/ImageToWebP"
        echo ""
        echo "You can now distribute this file without requiring Python!"
        echo ""
        
        # Ask if user wants to run the executable
        read -p "Do you want to test the executable now? (Y/N) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Starting executable..."
            ./dist/ImageToWebP
        fi
    fi
else
    echo ""
    echo "BUILD FAILED!"
    echo "Please check the error messages above."
    exit 1
fi
