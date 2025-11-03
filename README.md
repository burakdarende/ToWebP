# 🖼️ Image to WebP Converter

Modern, cross-platform GUI application for converting images to WebP format while maintaining folder structure.

## ✨ Features

- 🎨 **Modern Dark Theme UI** - Beautiful and intuitive interface
- 📁 **Folder Structure Preservation** - Maintains exact folder hierarchy
- 🔄 **Multiple Format Support** - Converts JPG, PNG, BMP, TIFF, GIF to WebP
- ⚙️ **Adjustable Settings** - Control quality, compression method, and lossless options
- 📊 **Real-time Progress** - Live conversion progress and detailed logging
- 💻 **Cross-Platform** - Works on Windows and macOS
- 🚀 **Standalone Executable** - No Python installation required for end users

## 🚀 Quick Start

### Option 1: Run from Source

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python gui.py
```

### Option 2: Build Executable

1. Install build dependencies:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

2. Build the executable:

```bash
python build_exe.py
```

3. Find your executable in the `dist` folder:
   - Windows: `dist/ImageToWebP.exe`
   - macOS: `dist/ImageToWebP.app`

## 📖 How to Use

1. **Select Source Folder**: Click "Browse" to choose a folder containing your images
2. **Adjust Settings**:
   - **Quality**: 1-100 (higher = better quality, larger file)
   - **Lossless**: Perfect quality but larger files
   - **Compression Level**: 0-6 (higher = better compression, slower)
3. **Start Conversion**: Click "🚀 Start Conversion"
4. **Check Output**: A new folder will be created with `_WebP` suffix containing all converted images

## 📂 Output Structure

Input folder structure:

```
C:/serkan-fotolar/
├── 2023/
│   ├── summer/
│   │   └── beach.jpg
│   └── winter/
│       └── snow.png
└── 2024/
    └── spring/
        └── flowers.jpg
```

Output folder structure:

```
C:/serkan-fotolar_WebP/
├── 2023/
│   ├── summer/
│   │   └── beach.webp
│   └── winter/
│       └── snow.webp
└── 2024/
    └── spring/
        └── flowers.webp
```

## 🛠️ Technical Details

### Supported Input Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- GIF (.gif)

### Technologies Used

- **Python 3.8+**
- **Pillow** - Image processing
- **CustomTkinter** - Modern GUI framework
- **PyInstaller** - Executable creation

## 📝 Requirements

### For Running from Source:

- Python 3.8 or higher
- See `requirements.txt` for Python packages

### For Building Executable:

- Additional package: `pyinstaller`

## 🔧 Development

### Project Structure

```
ToWebP/
├── gui.py              # GUI application
├── converter.py        # Core conversion logic
├── build_exe.py        # Build script for executable
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Building on Different Platforms

**Windows:**

```bash
python build_exe.py
```

**macOS:**

```bash
python3 build_exe.py
```

The build script automatically detects your platform and creates the appropriate executable.

## 💡 Tips

- Use **Lossless** mode for archival purposes or when quality is critical
- Use **Quality 75-85** for a good balance between file size and quality
- Higher **Compression Levels** take longer but produce smaller files
- The original files are never modified - only copies are created

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## ⚠️ Important Notes

- **Folder Naming**: Only the root output folder gets `_WebP` suffix, subdirectories keep original names
- **Non-Image Files**: Non-image files in the source folder are copied as-is
- **Memory Usage**: Processing very large images may require significant memory
- **Transparency**: Alpha channels are preserved in lossless mode, converted to white background in lossy mode

## 🆘 Troubleshooting

**Application doesn't start:**

- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Conversion fails:**

- Check that source folder exists and contains supported image formats
- Ensure you have write permissions for the output location

**Executable build fails:**

- Make sure PyInstaller is installed: `pip install pyinstaller`
- Try running with admin/sudo privileges

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for easy WebP conversion
