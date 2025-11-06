# Changelog

All notable changes to ImageToWebP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Custom icon support for executables
- Drag & drop support enhancement
- Additional image format support (HEIC, AVIF)
- Preset saving/loading for quick access

---

## [2.0.0] - 2025-11-06

### 🎉 Major Release - Premium UI v2.0

#### Added

- **Premium Modern Interface**

  - Tab-based navigation (Convert, Settings, Fine-Tuning, About)
  - Gradient color-themed stat cards
  - Collapsible sections for better space management
  - Responsive design (1000x700 to 1400x900)
  - Smooth hover effects and animations

- **Live Statistics Dashboard**

  - Real-time files processed counter
  - Conversion speed (images/sec)
  - Total space saved tracker
  - Elapsed time display
  - Color-coded gradient backgrounds

- **Animated Progress System**

  - Color-changing progress bar (Orange → Blue → Green)
  - Smooth progress animations
  - Percentage display

- **Enhanced Fine-Tuning Controls**

  - Auto Tone button for automatic adjustments
  - Manual controls: Contrast, Brightness, Vibrance, Saturation
  - Live preview updates
  - Reset to defaults option

- **Multi-Platform Builds**

  - Automated GitHub Actions workflow
  - Windows executable (.exe)
  - macOS app bundle (.app) + DMG installer
  - Linux binary (.tar.gz)

- **Build System**
  - Cross-platform build script (`build_exe.py`)
  - Platform-specific optimizations
  - macOS onedir mode for .app bundles
  - Windows onefile single executable

#### Changed

- Complete UI overhaul with modern design principles
- Improved color scheme and visual hierarchy
- Better space utilization with compact layouts
- Enhanced user experience with intuitive controls

#### Fixed

- macOS build icon error resolved
- PyInstaller deprecation warnings for macOS
- Progress callback parameter mismatch
- Format specifier errors in f-strings
- Fine-tuning parameter passing issues

#### Technical

- **Dependencies Updated:**

  - Python 3.10+ (from 3.8+)
  - CustomTkinter 5.2+
  - Pillow 10.0+
  - NumPy 1.24+
  - PyInstaller 6.16.0

- **Build Configuration:**

  - Windows: `--onefile` mode (single .exe)
  - macOS: `--onedir` mode (.app bundle)
  - Linux: `--onefile` mode (single binary)

- **GitHub Actions:**
  - Automated multi-platform builds
  - Automatic release creation with changelog
  - Artifact retention: 90 days
  - DMG creation for macOS with fallback to ZIP

---

## [1.0.0] - 2024

### Initial Release

#### Added

- Basic GUI interface for WebP conversion
- Single file and folder batch conversion
- Quality control (1-100)
- Lossless mode support
- Folder structure preservation
- Smart version numbering (\_WebP_2, \_WebP_3)
- Real-time progress logging
- Dark theme UI with CustomTkinter

#### Supported Formats

- Input: JPG, JPEG, PNG, BMP, TIFF, GIF
- Output: WebP

#### Features

- Multi-threading support
- Compression level control (0-6)
- Basic image adjustments
- Cross-platform compatibility (Windows, macOS, Linux)

---

## Version History

| Version | Release Date | Highlights                                     |
| ------- | ------------ | ---------------------------------------------- |
| 2.0.0   | 2025-11-06   | Premium UI, Live Statistics, Animated Progress |
| 1.0.0   | 2024         | Initial Release, Basic Conversion Features     |

---

## Upgrade Notes

### Upgrading to 2.0.0 from 1.0.0

**Breaking Changes:**

- None - Fully backward compatible

**New Requirements:**

- Python 3.10+ (was 3.8+)
- Updated dependencies (see requirements.txt)

**Migration:**

1. Download new version or update from source
2. No configuration changes needed
3. All previous features work as before
4. New Premium UI loads automatically

**What's New:**

- Premium UI with tabs and live stats
- Enhanced fine-tuning controls
- Animated progress visualization
- Multi-platform executable builds

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Support

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/burakdarende/ToWebP/issues)
- 💡 **Feature Requests:** [GitHub Issues](https://github.com/burakdarende/ToWebP/issues)
- 📧 **Contact:** [GitHub Discussions](https://github.com/burakdarende/ToWebP/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
