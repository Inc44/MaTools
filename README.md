# MaTools

Management Tools is a comprehensive GUI application built with PyQt6 that consolidates various tools for different tasks into one fast and efficient interface.

![Screenshot](screenshot.png)

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

Before you begin, ensure you have met the following requirements:

- Python 3.10/3.11 (Should also work for lower versions)
- Additional Python packages are installed (Run `pip install -r requirements.txt`)

### Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Inc44/MaTools.git
    ```

2. **Navigate to the Project Directory**
    ```bash
    cd MaTools
    ```

3. **Install Required Packages**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**
    ```bash
    python main_management_tools_app.pyw
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
