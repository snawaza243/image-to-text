# 🖼️ Image to Text Converter

A powerful desktop application that extracts text from images using **Optical Character Recognition (OCR)** technology.  
Built with **Python** and **Tkinter**, this tool provides a user-friendly interface for converting multiple images to text efficiently.

![Image to Text Converter](https://img.shields.io/badge/Version-2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

---

## ✨ Features

- 📷 Extract text from multiple image formats (**PNG, JPG, JPEG, GIF, BMP, TIFF**)
- 🖼️ User-friendly graphical interface with progress tracking
- 📁 Batch process multiple images in a folder
- 💾 Save extracted text to a file of your choice
- 🔍 Built-in Tesseract OCR engine (no separate installation required)
- 📊 Real-time progress monitoring
- 🎨 Modern, responsive UI design
- ⚡ Multi-threaded processing for responsive UI

---

## 🖼️ Screenshots
![Application Screenshot](screenshot.png)

---

## 🔧 Installation

### Method 1: Download Pre-built Executable
1. Go to the [Releases](https://github.com/IndianTechnoEra/ImageToTextConverter/releases) page  
2. Download the latest `ImageToTextConverter Setup.exe` file  
3. Run the installer and follow the setup instructions  
4. Launch the application from your desktop or start menu  

---

### Method 2: Build from Source

#### Prerequisites
- Python 3.6 or higher  
- Git  

#### Steps

```bash
# Clone the repository
git clone https://github.com/IndianTechnoEra/ImageToTextConverter.git
cd ImageToTextConverter

# Install required dependencies
pip install -r requirements.txt

# Run the application
python src/image_to_text_converter.py

```
## ▶ Usage

1. Select Image Folder: Click "Select Folder" to choose the folder containing your images
2. Choose Output File: Click "Select Output File" to specify where to save the extracted text
3. Convert Images: Click "Convert" to start the text extraction process
4. View Results: Once completed, click "Open Text File" to view the extracted text

## 🖼 Supported Image Formats
1. PNG (.png)
2. JPEG (.jpg, .jpeg)
3. GIF (.gif)
4. BMP (.bmp)
5. TIFF (.tiff)

## 🏗 Building the Executable
1. To build the executable yourself:
## Install PyInstaller
```
pip install pyinstaller
```
## Run the build script
```
python build.py
```

The executable will be created in the dist folder.

### 📂 Project Structure
```
ImageToTextConverter/
├── src/
│   └── image_to_text_converter.py  # Main application code
├── Tesseract-OCR/                  # Embedded OCR engine
├── dist/                           # Built executables
├── build.py                        # Build script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```
## 🛠 Technologies Used

1. Python: Core programming language

2. Tkinter: GUI framework

3. Pytesseract: Python wrapper for Tesseract OCR

4. Pillow (PIL): Image processing library

5. PyInstaller: Package to create executable files

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

# Fork the project
## Create your feature branch
```
git checkout -b feature/AmazingFeature
```
## Commit your changes
```
git commit -m "Add some AmazingFeature"
```

## Push to the branch
```
git push origin feature/AmazingFeature
```

Then open a Pull Request 🚀


# 💬 Support

1. If you encounter any issues or have questions:

2. Check the FAQ section below

3. Search existing issues

4. Create a new issue with details about your problem


## ❓ FAQ

Q: Does this application require internet connection?
A: No, all processing happens locally on your computer.

Q: What languages does the OCR support?
A: The application primarily supports English. Additional language packs can be added to the tessdata folder.

Q: Can I use this application commercially?
A: Yes, this application is open source and free for commercial use.

Q: The application is running slowly with many images. What can I do?
A: For large numbers of images, consider processing them in smaller batches.


# 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.


# 🙏 Acknowledgments

Tesseract OCR

Python community for excellent libraries and tools

Contributors who help improve this project


# 📬 Contact

IndianTechnoEra
📧 Email: indiantechnoera@gmail.com

🌐 Website: https://www.indiantechnoera.in

💻 GitHub: IndianTechnoEra

⭐ If you find this project helpful, please give it a star on GitHub!


# 📂 Additional Files Needed

1️⃣ requirements.txt
pillow>=8.0.0
pytesseract>=0.3.7
pyinstaller>=4.0


2️⃣ LICENSE
MIT License

Copyright (c) 2023 IndianTechnoEra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

3️⃣ .gitignore
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db


---
```


