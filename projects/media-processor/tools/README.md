# E-commerce Watermark Pro - Desktop App

A PyQt6 desktop application to visually position a watermark and batch process product images.

## Features

- Visual watermark positioning with drag & drop
- Smart resize to 1000x1000 with white padding
- Opacity and scale sliders
- Batch processing with progress bar
- Non-blocking UI during processing

## Requirements

- Python 3.10+
- PyQt6
- Pillow

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run from Python
```bash
python main.py
```

### Double-click Launcher
- **Windows**: `MediaProcessor.bat`
- **macOS**: `MediaProcessor.command` (run `chmod +x` first)

## Build Executable

### Windows
```bash
python -m PyInstaller --onefile --noconsole --name "MediaProcessor" main.py
```

### macOS
```bash
python -m PyInstaller --windowed --noconsole --name "MediaProcessor" main.py
```

The executable will be in the `dist/` folder.
