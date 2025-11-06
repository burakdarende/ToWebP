# 🏗️ Build Information

## ✅ Latest Build Status

### Windows Build

- **Status:** ✅ Success
- **File:** `ImageToWebP.exe`
- **Size:** ~23 MB
- **Location:** `dist/ImageToWebP.exe`
- **Build Date:** November 6, 2025
- **Python Version:** 3.10.6
- **PyInstaller Version:** 6.16.0

### macOS Build

- **Status:** ⏳ Not built yet (requires macOS system)
- **Expected File:** `ImageToWebP.app`
- **Expected Size:** ~25-30 MB

### Linux Build

- **Status:** ⏳ Not built yet
- **Expected File:** `ImageToWebP`
- **Expected Size:** ~25-30 MB

---

## 🔨 How to Build

### Prerequisites

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Build Commands

#### Windows:

```powershell
# Option 1: Using Python script
python build_exe.py

# Option 2: Using PowerShell script
.\build.ps1

# Option 3: Direct PyInstaller
pyinstaller --name=ImageToWebP --windowed --onefile --clean gui.py
```

#### macOS:

```bash
# Option 1: Using Python script
python3 build_exe.py

# Option 2: Using bash script
chmod +x build.sh
./build.sh

# Option 3: Direct PyInstaller
pyinstaller --name=ImageToWebP --windowed --onefile --clean gui.py
```

#### Linux:

```bash
# Using Python script
python3 build_exe.py

# Direct PyInstaller
pyinstaller --name=ImageToWebP --onefile --clean gui.py
```

---

## 📦 Build Output

After successful build, you'll find:

```
dist/
├── ImageToWebP.exe        # Windows executable (single file)
└── ImageToWebP.app        # macOS application bundle (on Mac)
```

Build artifacts (can be deleted):

```
build/                     # Temporary build files
ImageToWebP.spec          # PyInstaller specification file
```

---

## 🧪 Testing the Executable

### Windows:

```powershell
# Run from command line
.\dist\ImageToWebP.exe

# Or double-click ImageToWebP.exe in File Explorer
```

### macOS:

```bash
# Run from terminal
./dist/ImageToWebP.app/Contents/MacOS/ImageToWebP

# Or double-click ImageToWebP.app in Finder
```

### Linux:

```bash
# Make executable (if needed)
chmod +x dist/ImageToWebP

# Run
./dist/ImageToWebP
```

---

## 📊 Build Statistics

### Windows Build Performance:

- **Total Build Time:** ~20-25 seconds
- **Dependencies Bundled:** 934 entries
- **DLLs Included:** Python runtime, NumPy, Pillow, CustomTkinter, Tkinter
- **Compression:** Default

### File Size Breakdown:

- **Base Executable:** ~5 MB
- **Python Runtime:** ~8 MB
- **NumPy:** ~6 MB
- **Pillow:** ~2 MB
- **CustomTkinter + Tkinter:** ~2 MB

---

## 🚀 Distribution

### Windows:

1. Copy `dist/ImageToWebP.exe` to desired location
2. No Python installation required
3. No additional files needed
4. Can be distributed standalone

### macOS:

1. Copy `dist/ImageToWebP.app` to Applications folder
2. Or distribute as DMG file
3. May need to sign for Gatekeeper (optional)

### Linux:

1. Distribute the binary with instructions
2. May need to set executable permission
3. Consider creating .deb or .rpm package

---

## ⚠️ Known Issues

### Windows:

- First launch may be flagged by Windows Defender (add exception)
- Antivirus software may scan on first run (normal behavior)

### macOS:

- "App is damaged" warning on unsigned builds
  - Solution: `xattr -cr ImageToWebP.app`
- Gatekeeper may block unsigned apps
  - Solution: Right-click > Open > Open Anyway

### Linux:

- Some distros may require additional libraries
- GTK themes may affect appearance

---

## 🔧 Customization

### Adding an Icon:

**Windows:**

```python
# In build_exe.py, add:
args.append('--icon=icon.ico')
```

**macOS:**

```python
# In build_exe.py, add:
args.extend(['--icon=icon.icns'])
```

### Reducing File Size:

```python
# Add to build_exe.py:
args.extend([
    '--exclude-module=tkinter.test',
    '--exclude-module=unittest',
    '--exclude-module=email',
    '--exclude-module=http',
])
```

### Debug Build:

```python
# Change in build_exe.py:
# Replace '--windowed' with '--console'
# This shows console output for debugging
```

---

## 📝 Build Checklist

Before building:

- [ ] Update version in code
- [ ] Test all features work
- [ ] Update README.md
- [ ] Clean previous builds (`rmdir /s build dist`)
- [ ] Check all dependencies in requirements.txt

After building:

- [ ] Test executable on clean system
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Test with various image formats
- [ ] Create release notes

---

## 🎯 CI/CD Integration (Future)

For automated builds, consider:

- **GitHub Actions** - Build on multiple platforms
- **AppVeyor** - Windows builds
- **Travis CI** - macOS/Linux builds

Example GitHub Actions workflow:

```yaml
name: Build Executables

on: [push, pull_request]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: "3.10"
      - run: pip install -r requirements.txt pyinstaller
      - run: python build_exe.py
      - uses: actions/upload-artifact@v2
        with:
          name: ImageToWebP-Windows
          path: dist/ImageToWebP.exe

  build-macos:
    runs-on: macos-latest
    # Similar steps for macOS

  build-linux:
    runs-on: ubuntu-latest
    # Similar steps for Linux
```

---

**Last Updated:** November 6, 2025
**Build System:** PyInstaller 6.16.0
**Python Version:** 3.10.6
