# MaTools: A Comprehensive Management Toolkit

MaTools is an all-in-one GUI application, created using PyQt6, that offers a suite of tools for various tasks, all within an efficient, user-friendly interface.

![MaTools Screenshot](screenshot.png)

## 🌟 Features

- 🎵 Audio Speech Recognition*
- 📖 Optical Character Recognition
- 🎧 YouTube Audio Downloader
- 📝 PDF Merger
- 🎨 SVG to PNG Converter
- 🎬 FFmpeg Video Trim
- 🐍 Python Code Formatter
- 📂 File Sync
- 📅 Media Date Organizer
- 🔇 Silence Remover
- 🖼️ Image Trimmer
- 🛠️ And much more!

\* I would advise to pre-process the audio using [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)

## 🚀 Getting Started

### Prerequisites

- Python 3.10 (Python 3.11 only works for MaTools)
- Required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Installation Steps

1. Set up a single Conda environment:

    ```bash
    conda create --name MaTools python=3.11.5
    conda activate MaTools
    ```

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Inc44/MaTools.git
    ```

2. **Navigate into Project Directory**:
    ```bash
    cd MaTools
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create Conda Enviroments**:

    ```bash
    conda create --name whisperx python=3.10.13
    conda activate whisperx
    pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
    pip install git+https://github.com/m-bain/whisperx.git
    ```

    ```bash
    conda create --name ocrmypdf python=3.10.13
    conda activate ocrmypdf
    pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
    pip install ocrmypdf
    pip install git+https://github.com/ocrmypdf/OCRmyPDF-EasyOCR.git
    ```

5. **Launch the Application**:
    ```bash
    python main_management_tools_app.pyw
    ```

### Important Links

- [Anaconda](https://www.anaconda.com/download) - Conda GUI or [Miniconda](https://docs.conda.io/projects/miniconda/en/latest) - Conda CLI
- [Efficient Compression Tool](https://github.com/fhanau/Efficient-Compression-Tool.git) - Photo Compressor
- [ExifTool](https://exiftool.org/) - Metadata
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) - Media
- [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) - OCR processor
- [Unpaper](https://github.com/rodrigost23/unpaper/releases) - OCR preprocessor
- [yt-dlp](https://github.com/yt-dlp/yt-dlp.git) - Media downloader

### System Requirements

Ensure these binaries are in your system's PATH:

- `ect.exe` - Version 0.9.4 tested
- `exiftool.exe` - Version 12.59 tested
- `ffmpeg.exe` - Version 6.0 tested
- `unpaper.exe` (and its dlls) - Version 6.1 tested
- `yt-dlp.exe` - Version 2023.07.06 tested

#### Adding Binaries to System Path

1. Download the necessary binaries.
2. Include them in your system's PATH, e.g., `C:\Windows\`.

Check their presence:

```bash
ect.exe --version
exiftool.exe -ver
ffmpeg.exe -version
yt-dlp.exe --version
unpaper --version
```

## 🛠️ Usage

After launching, the toolbar at the top showcases icons for various tools. Hover over an icon to see its description. Click to activate the respective tool.

## 🎨 Customization

MaTools allows theme tweaks. To modify the theme, adjust the `theme_name` variable in the main script:

```python
theme_name = "white_flat_theme"  # Choose your preferred theme
```

## 🤝 Contribution

Contributions are heartily welcomed! If you're considering significant modifications, please initiate an issue for discussions before submitting a pull request.

## 📜 License

This software is under the GNU General Public License v3.0 (GPL-3.0). For comprehensive details, refer to [LICENSE.md](LICENSE.md).