# {{WORKFLOW_TITLE}} - Desktop App

A PyQt6 desktop application for {{WORKFLOW_DESCRIPTION}}.

## Features

- Feature 1
- Feature 2
- Progress tracking with status updates
- Non-blocking UI during processing

## Requirements

- Python 3.10+
- PyQt6
- Pillow
- Pandas + openpyxl

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
- **Windows**: `Launcher.bat`
- **macOS**: `Launcher.command` (run `chmod +x` first)

## Build Executable

### Windows
```bash
python -m PyInstaller --onefile --noconsole --name "{{APP_NAME}}" main.py
```

### macOS
```bash
python -m PyInstaller --windowed --noconsole --name "{{APP_NAME}}" main.py
```

The executable will be in the `dist/` folder.
