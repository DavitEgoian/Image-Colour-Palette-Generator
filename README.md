# 🎨 Image Colour Palette Generator

A powerful Python desktop application that analyzes images to identify the most common colors and generates a professional hex-code palette.

## 📝 Project Overview

Inspired by design tools like Flat UI Colors, this application uses local image processing to generate designer-ready color swatches. Simply load an image, view the extracted colors in real-time, and export your palette for use in your design projects.

## 🚀 Features

- **Smart Extraction**: Uses **PIL (Pillow)** and `collections.Counter` to algorithmically identify the top 10 most frequent RGB values in any image.
- **Modern GUI**: A responsive interface built with **PyQt5**, featuring intuitive toolbars, progress indicators, and native file dialogs.
- **Live Preview**: Instantly visualize your uploaded image alongside the generated color swatches.
- **One-Click Export**: Save your palette as a high-quality PNG file (automatically named `palette_YYYYMMDD_HHMMSS.png`).

## 💻 Installation & Usage

### Prerequisites
- Python 3.x

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/DavitEgoian/Image-Colour-Palette-Generator.git
   cd Image-Colour-Palette-Generator
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install Pillow PyQt5
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 📂 Project Structure

```text
image-palette-generator/
├── color_extractor.py    # Core logic: extracts top N colors from a PIL.Image
├── palette_saver.py      # Export logic: renders and saves swatch strip as PNG
└── main.py               # Interface: PyQt5 GUI for loading, viewing, and saving
```

## ⚙️ Customization

You can easily tweak the code to fit your needs:

- **Number of Colors**: Adjust the `top_colors(num=10)` argument in `color_extractor.py` to change how many colors are generated.
- **Swatch Dimensions**: Modify `swatch_size` in `palette_saver.py` to change the pixel size of the exported color blocks.
- **UI Enhancements**: Edit `main.py` to add new toolbar icons, shortcuts, or drag-and-drop functionality.

## 📄 License

This project is open source and available for personal and educational use.
