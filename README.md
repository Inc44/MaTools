# MaTools

Certainly! Below is a README template that explains how to set up and use your "Management Tools" application, which appears to be a PyQt6-based GUI offering various functionalities. Feel free to customize this further to suit the exact nature of your application.

---

# Management Tools

Management Tools is a comprehensive GUI application built with PyQt6 that consolidates various tools for different tasks into one fast and efficient interface.

![Screenshot](screenshot.png)  <!-- Update this path to an actual screenshot of your app -->

## Features

- File Sync
- Media Date Organizer
- PDF Merger
- Python Code Formatter
- Sort Lines
- SVG To PNG Converter
- And many more!

## Getting Started

### Prerequisites

- Python 3.11 (Probably work for lower versions)
- PyQt6 (GUI)
- black (Code formatter)
- img2pdf (Image to PDF converter)
- exif (EXIF data extractor)
- pyexifinfo (EXIF data extractor)
- PyPDF2 (PDF file manipulator)
- yt-dlp (Media Downloader)

```bash
pip install PyQt6
```

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepositoryname.git
    ```
2. Navigate to the project directory:
    ```bash
    cd yourrepositoryname
    ```
3. Install required packages:
    ```bash
    pip install -r requirements.txt  # If you have a requirements file
    ```
4. Run the application:
    ```bash
    python main.py  # Update this if your main file is named differently
    ```

## How to Use

The application opens with a toolbar at the top, which contains icons for all the different tools. Hover over an icon to see a tooltip describing what that tool does. Click an icon to open the corresponding tool.

## Customizing Themes

The application supports themes. You can change the theme by modifying the `theme_name` variable in the main file.

```python
theme_name = "white_flat_theme"  # Change this to another theme name
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

This README template should provide a good starting point for your project. Make sure to replace placeholders like `yourusername` and `yourrepositoryname` with the actual GitHub username and repository name.
