# {{WORKFLOW_NAME}} - Prompt Guide

This guide contains the recommended prompts to build the "{{WORKFLOW_TITLE}}" tool using an AI coding assistant.

## Phase 1: Core Logic (Python Script)

Use this prompt to build the fundamental processing logic.

```markdown
I have `input-file.xlsx` (with '{{COLUMN_NAME}}' column) and `template.png`. Write a Python script using Pillow/Pandas to:

**Input Handling:**
- Load data from Excel/CSV file.
- Validate required columns exist.
- Handle missing or invalid data gracefully.

**Processing:**
- [Describe the main processing logic here]
- Support Unicode characters (Vietnamese, Chinese, etc.).

**Output:**
- Save results to `output/` folder.
- Print progress log (e.g., 'Processed 1/200: Item Name').
```

## Phase 2: Desktop App (GUI)

Use this prompt to wrap the logic into a user-friendly desktop application.

```markdown
**Role:** Python GUI Developer (PyQt6 Specialist)
**Task:** Create "{{WORKFLOW_TITLE}}" Desktop App

**Objective:** A visual tool to [describe main objective].

**Tech Stack:**
* Language: Python 3.10+
* GUI Library: PyQt6 (Cross-platform)
* Graphics: Pillow (drawing), Pandas (data)
* Packaging: PyInstaller

**Functional Requirements:**
1.  **UI Layout (PyQt6):**
    *   **Tab 1 - Design/Config:**
        *   [Describe configuration options]
        *   [Describe visual preview if applicable]
    *   **Tab 2 - Process/Generate:**
        *   Load input file.
        *   "Process" Button and Progress Bar.

2.  **Core Logic:**
    *   [Describe core processing logic]
    *   **Threading:** Processing loop runs in `QThread` to prevent UI freeze.

3.  **Deliverables:**
    *   `main.py`: Complete source code.
    *   `requirements.txt`: Dependencies (PyQt6, Pillow, Pandas, openpyxl, pyinstaller).
    *   **Launcher Scripts (double-click to run):**
        *   Windows: `Launcher.bat`
            ```batch
            @echo off
            cd /d "%~dp0"
            python main.py
            ```
        *   macOS: `Launcher.command`
            ```bash
            #!/bin/bash
            cd "$(dirname "$0")"
            python3 main.py
            ```
            (Run `chmod +x Launcher.command` first)
```

**Build Executable (optional, for distribution):**
*   Windows (.exe): `python -m PyInstaller --onefile --noconsole --name "{{APP_NAME}}" main.py`
*   macOS (.app): `python -m PyInstaller --windowed --noconsole --name "{{APP_NAME}}" main.py`
*   Output in `dist/` folder.
*   Note: Must build on target OS (Windows for .exe, macOS for .app).
