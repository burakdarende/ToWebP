#!/bin/bash
# Quick Start Script for macOS/Linux
# Run this script to start the application

echo ""
echo "========================================"
echo "   Image to WebP Converter"
echo "========================================"
echo ""

# Check if Python is installed
echo "Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python from: https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit"
    exit 1
fi

echo "Python found!"
echo ""

# Check and install requirements
echo "Checking dependencies..."

python3 -c "import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies!"
        echo ""
        read -p "Press Enter to exit"
        exit 1
    fi
fi

echo "All dependencies ready!"
echo ""

# Run the application
echo "Starting application..."
echo ""

python3 gui.py

echo ""
echo "Application closed."
