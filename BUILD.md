# 🔧 Build Instructions

## Local Build

### Prerequisites

- Python 3.10+
- All dependencies from `requirements.txt`
- PyInstaller 6.0+

### Quick Build

```bash
# Install build dependencies
pip install pyinstaller

# Build for your platform
python build_exe.py
```

**Output locations:**

- **Windows:** `dist/ImageToWebP.exe` (~23 MB) - Single file executable
- **macOS:** `dist/ImageToWebP.app` (app bundle directory) - ~30-40 MB
- **Linux:** `dist/ImageToWebP` (executable) - ~25-30 MB

**Note:** macOS builds use `--onedir` mode (app bundle) instead of `--onefile` to comply with macOS security requirements and avoid PyInstaller deprecation warnings.

---

## GitHub Actions (Automated Multi-Platform Build)

### Using GitHub Actions

The repository includes automated builds for **Windows**, **macOS**, and **Linux**.

#### Option 1: Manual Trigger (Recommended)

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Build Executables** workflow
4. Click **Run workflow** button
5. Wait for builds to complete (~5-10 minutes)
6. Download artifacts from workflow run

#### Option 2: Tag-Based Release (Automatic)

Create a version tag to trigger automated build + release:

```bash
# Create and push a version tag
git tag v2.0.0
git push origin v2.0.0
```

This will:

- ✅ Build executables for Windows, macOS, Linux
- ✅ Create GitHub Release automatically
- ✅ Attach executables to the release
- ✅ Make them publicly downloadable

---

## Build Outputs

### Windows

- **File:** `ImageToWebP.exe`
- **Size:** ~22-24 MB
- **Standalone:** No Python installation required
- **Features:** Full Premium UI with all features

### macOS

- **File:** `ImageToWebP.app` (app bundle) + `ImageToWebP.dmg` (installer)
- **Size:** ~30-40 MB (.app bundle), ~20-25 MB (.dmg compressed)
- **Format:** Native .app bundle packaged in .dmg installer
- **Mode:** `--onedir` (directory bundle, recommended for macOS)
- **Compatibility:** macOS 10.13+ (ARM64 and Intel supported)
- **Note:** Uses onedir mode to avoid PyInstaller v7 deprecation and macOS security issues

### Linux

- **File:** `ImageToWebP` (tarball)
- **Size:** ~25-30 MB
- **Format:** Executable binary
- **Dependencies:** May require `python3-tk` on some systems

---

## Build Configuration

The build process is configured in `build_exe.py`:

**Common Arguments:**
- `--windowed` - No console window (GUI only)
- `--clean` - Clean PyInstaller cache
- `--noconfirm` - No confirmation prompts
- `--name` - Executable name: ImageToWebP

**Platform-Specific:**
- **Windows:** `--onefile` (single .exe file)
- **macOS:** `--onedir` (app bundle directory)
- **Linux:** `--onefile` (single binary)

**Why onedir for macOS?**
- Avoids PyInstaller v7 deprecation warnings
- Complies with macOS security and code signing
- Standard format for macOS applications (.app bundles)

### Customizing Build

Edit `build_exe.py` to customize:

```python
# Add custom icon
'--icon=icon.ico',

# Include additional data files
'--add-data=assets;assets',

# Exclude modules to reduce size
'--exclude-module=matplotlib',
```

---

## Troubleshooting

### Build Fails on Windows

```bash
# Clean previous builds
rm -r build dist *.spec

# Reinstall PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# Try again
python build_exe.py
```

### macOS Code Signing (Optional)

For distribution outside App Store:

```bash
# Sign the app
codesign --force --deep --sign - dist/ImageToWebP.app

# Create notarized DMG (requires Apple Developer account)
xcrun notarytool submit ImageToWebP.dmg --apple-id your@email.com
```

### Linux Compatibility Issues

If users encounter missing libraries:

```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On Fedora
sudo dnf install python3-tkinter

# On Arch
sudo pacman -S tk
```

---

## GitHub Actions Setup

The workflow file is located at: `.github/workflows/build.yml`

**Triggers:**

- ✅ Manual dispatch (workflow_dispatch)
- ✅ Push to tags matching `v*` (e.g., v2.0.0, v2.1.0)

**Jobs:**

1. `build-windows` - Builds Windows .exe
2. `build-macos` - Builds macOS .app + .dmg
3. `build-linux` - Builds Linux binary + tarball

**Artifacts:**

- Retained for 90 days
- Named: `ImageToWebP-{Platform}-{Version}`

**Release Creation:**

- Automatically creates GitHub Release on tag push
- Attaches all platform executables
- Sets as non-draft, non-prerelease

---

## Version Management

### Recommended Versioning

```bash
# Major release (breaking changes)
git tag v2.0.0

# Minor release (new features)
git tag v2.1.0

# Patch release (bug fixes)
git tag v2.0.1

# Beta/Alpha releases
git tag v2.0.0-beta.1
git tag v2.1.0-alpha.2
```

### Push Tags

```bash
# Push specific tag
git push origin v2.0.0

# Push all tags
git push --tags
```

---

## Distribution

### Direct Download (GitHub Releases)

Users can download from:

```
https://github.com/yourusername/ToWebP/releases/latest
```

### Manual Distribution

After local build:

1. Compress executable: `zip ImageToWebP-Windows.zip dist/ImageToWebP.exe`
2. Upload to your hosting/cloud storage
3. Share download link

### Checksum Generation (Security)

```bash
# Windows (PowerShell)
Get-FileHash dist\ImageToWebP.exe -Algorithm SHA256

# macOS/Linux
shasum -a 256 dist/ImageToWebP.app
```

Include checksums in release notes for verification.

---

## Performance Notes

**Build Time:**

- Local: ~1-2 minutes
- GitHub Actions: ~5-10 minutes per platform

**Executable Size:**

- Includes: Python runtime, all libraries, Premium UI assets
- CustomTkinter: ~5 MB
- Pillow + NumPy: ~10 MB
- Python runtime: ~8 MB

**Optimization Options:**

To reduce size (optional):

```python
# In build_exe.py, add:
'--exclude-module=tkinterdnd2',  # If drag-drop not needed
'--exclude-module=psutil',       # If system stats not needed
```

This can reduce size by ~3-5 MB.

---

## Premium UI v2.0 Features in Build

All features included in executable:

- ✅ Tab-based navigation
- ✅ Live statistics dashboard
- ✅ Animated progress bars
- ✅ Gradient color themes
- ✅ Dark mode support
- ✅ Batch processing
- ✅ Fine-tuning controls
- ✅ Multi-threading support

**No external files required** - everything is bundled!

---

## Support

Build issues? Check:

1. Python version (3.10+ required)
2. PyInstaller version (6.0+ recommended)
3. All requirements.txt dependencies installed
4. Sufficient disk space (~500 MB for temp files)

For GitHub Actions issues:

- Check workflow logs in Actions tab
- Verify GITHUB_TOKEN permissions
- Ensure tag format matches `v*` pattern
