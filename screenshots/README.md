# 📸 Screenshots Directory

This folder contains screenshots for the project README.

## Required Screenshots:

### 1. main-interface.png

- **What to capture:** Full application window showing:
  - Source folder/file selection
  - Quality settings
  - Resize options
  - Fine-tuning checkbox
  - Convert button
  - Progress area

**How to take:**

1. Run `python gui.py`
2. Don't select any folder yet (keep it clean)
3. Take full window screenshot
4. Save as `main-interface.png` (700-800px width recommended)

### 2. fine-tuning.png

- **What to capture:** Fine-tuning dialog window showing:
  - Auto Tone checkbox
  - All slider controls
  - Reset button
  - Apply button

**How to take:**

1. Click "Open Fine-Tuning Adjustments" button
2. Screenshot the dialog window
3. Save as `fine-tuning.png` (500px width recommended)

### 3. processing.png

- **What to capture:** Application during conversion showing:
  - STOP button (red)
  - Progress bar filled
  - Log messages in the text area

**How to take:**

1. Select a folder with a few images
2. Click "Start Conversion"
3. Quickly screenshot while it's processing
4. Save as `processing.png` (700-800px width recommended)

## Screenshot Tips:

- Use **Windows Snipping Tool** (Win + Shift + S) or **macOS Screenshot** (Cmd + Shift + 4)
- Capture in **high resolution** (but save optimized for web)
- Keep screenshots **clean** - no desktop clutter in background
- Consider using **PNG format** for crisp text
- Optimal width: 500-800px (GitHub auto-scales)

## Optional Screenshots:

### 4. comparison.png (Before/After)

- Side-by-side comparison of original vs WebP
- Show file size reduction

### 5. folder-structure.png

- File explorer showing input/output folders
- Demonstrates \_WebP suffix and versioning

### 6. settings-examples.png

- Different quality settings and results
- Helpful for users choosing settings

---

**Note:** After adding screenshots, commit them to the repository:

```bash
git add screenshots/
git commit -m "Add screenshots for README"
git push
```

Then they will be visible on GitHub!
