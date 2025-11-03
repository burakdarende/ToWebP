"""
Build script for creating executable
Run this to create standalone executable for Windows/Mac
"""
import PyInstaller.__main__
import sys
import os

def build():
    """Build the executable"""
    
    # Get the platform
    platform = sys.platform
    
    # Base PyInstaller arguments
    args = [
        'gui.py',                       # Main script
        '--name=ImageToWebP',           # Application name
        '--windowed',                   # No console window (GUI app)
        '--onefile',                    # Single file executable
        '--clean',                      # Clean PyInstaller cache
        '--noconfirm',                  # Replace output directory without asking
    ]
    
    # Platform-specific settings
    if platform == 'darwin':  # macOS
        args.extend([
            '--icon=NONE',
            '--osx-bundle-identifier=com.imagetowebp.converter',
        ])
    elif platform == 'win32':  # Windows
        # You can add an icon here if you have one
        # args.append('--icon=icon.ico')
        pass
    
    print("=" * 60)
    print(f"Building executable for {platform}")
    print("=" * 60)
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("=" * 60)
    print("Build complete!")
    print(f"Executable location: dist/ImageToWebP")
    print("=" * 60)

if __name__ == '__main__':
    build()
