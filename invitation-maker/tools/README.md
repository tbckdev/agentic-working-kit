# Bulk Invitation Generator - Desktop App

A PyQt6 desktop application to design invitation layouts and batch-generate personalized image files.

## Features

- **Visual Design Tab**: Load template image, drag-drop to position text
- **Font Customization**: Choose font family, size, and color
- **Batch Generation**: Load guest list from Excel/CSV and generate all invitations
- **Progress Tracking**: Real-time progress bar with status updates
- **Threading**: Non-blocking UI during batch processing

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

```bash
python main.py
```

### Tab 1: Design
1. Click "Load Template" to select your invitation background image
2. Drag the "Placeholder Name" text box to set the position
3. Configure font settings (family, size, color)

### Tab 2: Generate
1. Load guest list (Excel .xlsx or CSV with 'Name' column)
2. Select output folder
3. Click "Generate Invitations"

## Build Executable

### Windows
```bash
pyinstaller --onefile --noconsole --name "InvitationMaker" main.py
```

### macOS
```bash
pyinstaller --windowed --noconsole --name "InvitationMaker" main.py
```

The executable will be in the `dist/` folder.
