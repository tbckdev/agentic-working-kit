# Media Processor - Prompt Guide

This guide contains the recommended prompts to build the "Smart Image Processor" tool using an AI coding assistant.

## Phase 1: Commander (Quick Fix)

For a quick one-off batch processing.

```markdown
I have a folder named `input` containing varied product images (JPG, PNG). I also have a `watermark.png` file.

Write a robust Python script using Pillow to process these images:

**Smart Resize:**
- Resize every image to fit within a 1000x1000 pixel canvas without cropping.
- Maintain original aspect ratio.
- Fill any empty space with a white background.
- Ensure the final output is exactly 1000x1000.

**Watermark:**
- Overlay `watermark.png` in the center of the image.
- Auto-scale: If the watermark is larger than 30% of the canvas width, resize it down to 30% width (maintain aspect ratio).
- Apply 70% opacity to the watermark.

**Output:**
- Save processed images to an `output` folder as JPG (quality=90).
- Handle RGBA to RGB conversion correctly.
- Print a progress log (e.g., 'Processed 1/500...').
- Skip corrupt images with warning.
```

**Result:** A script that processes 500 images in < 1 minute with full error handling.

## Phase 2: Architect (Permanent Tool)

For regular use by content teams.

```markdown
**Role:** Python GUI Developer (PyQt6 Specialist)
**Task:** Create a Cross-Platform Desktop App named "E-commerce Watermark Pro".

**Objective:** A standalone desktop tool to visually position a watermark on a base image and batch process a folder of images.

**Tech Stack:**
* Language: Python 3.10+
* GUI Library: PyQt6 (Must ensure cross-platform compatibility for Windows & macOS).
* Image Processing: Pillow (PIL).
* Packaging: PyInstaller.

**Functional Requirements:**
1.  **UI Layout (PyQt6):**
    *   Left Panel: Controls (Load Images, Opacity/Scale Sliders, Start Button).
    *   Right Panel: Interactive Canvas (QGraphicsScene) for Drag & Drop positioning of the watermark.
    *   *Constraint:* Use standard PyQt6 widgets so they render natively on both OS.

2.  **Batch Processing Logic:**
    *   Smart Resize to 1000x1000 (White padding).
    *   Apply watermark based on visual coordinates.
    *   Multithreading: Use `QThread` to prevent the UI from freezing during batch processing.

3.  **Deliverables:**
    *   `main.py`: Complete source code.
    *   `requirements.txt`: Dependencies (PyQt6, Pillow, pyinstaller).
    *   **Launcher Scripts (double-click to run):**
        *   Windows: `MediaProcessor.bat`
            ```batch
            @echo off
            cd /d "%~dp0"
            python main.py
            ```
        *   macOS: `MediaProcessor.command`
            ```bash
            #!/bin/bash
            cd "$(dirname "$0")"
            python3 main.py
            ```
            (Run `chmod +x MediaProcessor.command` first)
```

**Build Executable (optional, for distribution):**
*   Windows (.exe): `python -m PyInstaller --onefile --noconsole --name "MediaProcessor" main.py`
*   macOS (.app): `python -m PyInstaller --windowed --noconsole --name "MediaProcessor" main.py`
*   Output in `dist/` folder.
*   Note: Must build on target OS (Windows for .exe, macOS for .app).
