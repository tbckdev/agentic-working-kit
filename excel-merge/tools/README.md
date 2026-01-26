# Excel Merge Master - Desktop App

A PyQt6 desktop application to merge multiple Excel files into a single master report.

## Features

- Browse folder to select Excel files
- Auto-detect and skip temp files (~$)
- Add Source_File column for traceability
- Handle corrupted/locked files gracefully
- Real-time progress and log display

## Requirements

- Python 3.10+
- PyQt6
- Pandas + openpyxl + xlrd

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
- **Windows**: `ExcelMerge.bat`
- **macOS**: `ExcelMerge.command` (run `chmod +x` first)

## Build Executable

### Windows
```bash
python -m PyInstaller --onefile --noconsole --name "ExcelMerge" main.py
```

### macOS
```bash
python -m PyInstaller --windowed --noconsole --name "ExcelMerge" main.py
```

The executable will be in the `dist/` folder.
