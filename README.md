# 🖼️ Image Processing GUI Project

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/) [![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html) [![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org/) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Python desktop application built with **Tkinter** that provides an intuitive GUI interface for advanced image processing operations. This tool offers a wide range of image processing capabilities including color manipulation, filtering, edge detection, morphological operations, and more.

## 📋 Table of Contents

<table width="100%">
<tr>
<td width="33.33%"><a href="#-features">✨ Features</a></td>
<td width="33.33%"><a href="#-prerequisites">🔧 Prerequisites</a></td>
<td width="33.34%"><a href="#-installation">🚀 Installation</a></td>
</tr>
<tr>
<td width="33.33%"><a href="#-usage">💻 Usage</a></td>
<td width="33.33%"><a href="#-project-structure">📁 Project Structure</a></td>
<td width="33.34%"><a href="#-architecture-overview">🏗️ Architecture Overview</a></td>
</tr>
<tr>
<td width="33.33%"><a href="#-contributing">🤝 Contributing</a></td>
<td width="33.33%"><a href="#-license">📄 License</a></td>
<td width="33.34%"><a href="#-contact">📧 Contact</a></td>
</tr>
</table>

## ✨ Features

### 📂 File Management

- **Open Image**: Multiple formats
- **Save Image**: Export options

### 📊 Image Analysis

- **Histogram Display**: Grayscale & RGB
- **Real-time Updates**: Live histogram
- **Channel Analysis**: Individual RGB channels

---

### 🎨 Color Processing

- **RGB Color Filters**: 7+ color options
- **Color Space Conversion**: Multiple methods
- **Brightness & Contrast**: Adjustable controls

### 🔧 Image Enhancement

- **Histogram Equalization**: Contrast improvement
- **Fuzzy Processing**: Advanced operations
- **Noise Reduction**: Multiple algorithms

---

### ➕ Arithmetic Operations

- **Image Addition**: Blend images
- **Image Subtraction**: Difference ops
- **Image Multiplication**: Feature enhancement
- **Image Division**: Region normalization

### 🧩 Filtering Operations

- **Basic Filters**: Identity, Sharpen
- **Blur Filters**: Gaussian, Average
- **Advanced Filters**: Unsharp, Low/High-pass

---

### 🔍 Edge Detection

- **Prewitt Operator**: Edge detection
- **Sobel Operator**: Enhanced filtering

### 🔲 Morphological Operations

- **Erosion**: Multiple structuring elements
- **Dilation**: Various kernel sizes
- **Opening & Closing**: Complete operations

### ⚙️ Advanced Features

- **Color Inversion**: Advanced processing
- **Gamma Correction**: Professional tools
- **Bit Depth Reduction**: 1–7 bit options

## 🔧 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/hajuenter/image_processing_project.git
   cd PROJECT_UTS
   ```

2. **Create and activate virtual environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 💻 Usage

1. **Launch the application** by running `python main.py`
2. **Open an image** using the File menu
3. **Select desired operation** from the menu bar
4. **View results** in real-time
5. **Save processed image** using File → Save

### Quick Start Example

```python
# Example of running the application
# Navigate to PROJECT_UTS directory
cd PROJECT_UTS

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Run the application
python main.py
```

## 📁 Project Structure

```
PROJECT_UTS/
├── main.py                 # Main application entry point
├── main_window.py          # Main GUI window
├── features/               # Core features and utilities
├── icons/                  # Application icons and images
├── ui/                     # User Interface components
│   └── menu/               # Menu system
│       └── menu_bar.py     # Main menu bar
├── navbar/                 # Navigation components
│   ├── menu_about.py       # About dialog
│   ├── menu_arithmetic.py  # Arithmetic operations
│   ├── menu_colors.py      # Color processing
│   ├── menu_edge.py        # Edge detection
│   ├── menu_file.py        # File operations
│   ├── menu_filter.py      # Image filters
│   ├── menu_morfologi.py   # Morphological operations
│   ├── menu_processing.py  # Image processing
│   └── menu_view.py        # View operations
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore file
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 🏗️ Architecture Overview

Aplikasi ini menggunakan arsitektur modular dengan pemisahan yang jelas antara:

- **`main.py`**: Entry point aplikasi
- **`main_window.py`**: Window utama aplikasi
- **`ui/menu/`**: Sistem menu utama
- **`navbar/`**: Komponen-komponen menu yang spesifik untuk setiap fitur:
  - File operations (`menu_file.py`)
  - Color processing (`menu_colors.py`)
  - Image filters (`menu_filter.py`)
  - Edge detection (`menu_edge.py`)
  - Morphological operations (`menu_morfologi.py`)
  - Arithmetic operations (`menu_arithmetic.py`)
  - View operations (`menu_view.py`)
  - Image processing (`menu_processing.py`)
  - About dialog (`menu_about.py`)
- **`features/`**: Core utilities dan helper functions
- **`icons/`**: Asset gambar dan ikon untuk GUI

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation as needed
- Each menu functionality is separated into its own module for better maintainability

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📄 License

**Developer**: [bahrulahmad1945@gmail.com](mailto:bahrulahmad1945@gmail.com)

- GitHub: [@hajuenter](https://github.com/hajuenter)
- Project Link: [https://github.com/hajuenter/image_processing_project](https://github.com/hajuenter/image_processing_project)

## 🙏 Acknowledgments

- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
- Image processing powered by [OpenCV](https://opencv.org/)
- Mathematical operations using [NumPy](https://numpy.org/)
- Special thanks to the Python imaging community

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

</div>
