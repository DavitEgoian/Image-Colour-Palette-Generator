# 🎨 Image Colour Palette Generator

A Python program that finds the most common colours in an uploaded image.

## 📝 Project Overview

Inspired by online palette tools like Flat UI Colors, this Python application uses local image processing to generate a designer-ready list of HEX swatches. Users simply load an image, view the extracted palette, and export it as a PNG.

## 🚀 Features

- **Top 10 Colour Extraction**  
  Uses **PIL** and `collections.Counter` to find your image’s ten most frequent RGB values.

- **Modern GUI**  
  Beautiful, responsive interface built with **PyQt5**, featuring toolbars, progress indicators, and custom dialogs.

- **Live Preview**  
  See your uploaded image and its palette instantly in the app window.

- **One-Click Export**  
  Save the palette as a PNG file named `palette_YYYYMMDD_HHMMSS.png` by default.

## 💻 Installation & Usage

1. **Install dependencies**  
   ```bash
   pip install Pillow PyQt5
   ```

3. **Run the app**  
   ```bash
   python main.py
   ```

## 📂 Project Structure

```
image-palette-generator/
├── color_extractor.py    # Extracts top N colours from a PIL.Image
├── palette_saver.py      # Renders and saves swatch strip as PNG
└── main.py               # PyQt5 GUI: load image, display palette, save output
```

## ⚙️ Customization

- **Number of Colours**  
  Adjust the `top_colors()` default argument in **`color_extractor.py`** (e.g. `num=5` for a five-colour palette).

- **Swatch Size**  
  Change `swatch_size` in **`PaletteSaver`** to modify each hue block’s dimensions.

- **GUI Layout**  
  Modify toolbar icons, button actions, or add drag-and-drop support by editing **`main.py`**.

---
