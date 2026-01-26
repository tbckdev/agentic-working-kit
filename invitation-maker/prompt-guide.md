# Invitation Maker - Prompt Guide

This guide contains the recommended prompts to build the "Bulk Invitation Generator" tool using an AI coding assistant (like Claude, ChatGPT, or Cursor).

## Phase 1: Core Logic (Python Script)

Use this prompt to build the fundamental image processing and text rendering logic.

```markdown
I have `guests.csv` (with 'Name' column) and `template.jpg`. Write a Python script using Pillow to:

**Font Handling:**
- Try loading `custom_font.ttf` from the same folder.
- Fallback to system Arial or DejaVuSans if not found.
- Use font size 60px.

**Text Rendering:**
- Draw each name at position (500, 300) in Red (#FF0000).
- Auto-fit: If name is longer than 20 characters, reduce font size to fit within 400px width.
- Support Unicode characters (Vietnamese, Chinese, etc.).

**Output:**
- Save as `output/Invite_{Name}.jpg` (sanitize filename for special characters).
- Print progress log (e.g., 'Generated 1/200: Nguyen Van A').
```

## Phase 2: Desktop App (GUI)

Use this prompt to wrap the logic into a user-friendly desktop application.

```markdown
**Role:** Python GUI Developer (PyQt6 Specialist)
**Task:** Create "Bulk Invitation Generator" Desktop App

**Objective:** A visual tool to design invitation layouts and clear-generate hundreds of personalized image files.

**Tech Stack:**
* Language: Python 3.10+
* GUI Library: PyQt6 (Cross-platform)
* Graphics: Pillow (drawing), Pandas (data)
* Packaging: PyInstaller

**Functional Requirements:**
1.  **UI Layout (PyQt6):**
    *   **Tab 1 - Design:**
        *   Canvas to load Template Image.
        *   **Interactive Dragger:** Drag a "Placeholder Name" text box to set (X, Y) coordinates.
        *   **Properties:** Font Family (Dropdown), Size (Spinbox), Color (Color Dialog).
    *   **Tab 2 - Generate:**
        *   Load CSV (Guests).
        *   "Generate" Button and Progress Bar.

2.  **Core Logic:**
    *   Capture X,Y coordinates relative to image size from the Design tab.
    *   Map font settings to Pillow `ImageDraw` commands.
    *   **Threading:** Generation loop runs in `QThread` to prevent UI freeze.

3.  **Deliverables:**
    *   `main.py`: Complete source code.
    *   `requirements.txt`: Dependencies (PyQt6, Pillow, Pandas, openpyxl, pyinstaller).
    *   **Launcher Scripts (double-click to run):**
        *   Windows: `InvitationMaker.bat`
            ```batch
            @echo off
            cd /d "%~dp0"
            python main.py
            ```
        *   macOS: `InvitationMaker.command`
            ```bash
            #!/bin/bash
            cd "$(dirname "$0")"
            python3 main.py
            ```
            (Run `chmod +x InvitationMaker.command` first)
```
**Build Executable (optional, for distribution):**
*   Windows (.exe): `python -m PyInstaller --onefile --noconsole --name "InvitationMaker" main.py`
*   macOS (.app): `python -m PyInstaller --windowed --noconsole --name "InvitationMaker" main.py`
*   Output in `dist/` folder.
*   Note: Must build on target OS (Windows for .exe, macOS for .app).
