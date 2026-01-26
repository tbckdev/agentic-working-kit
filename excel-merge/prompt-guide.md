# Excel Merge - Prompt Guide

This guide contains the recommended prompts to build the "Excel Merge Master" tool using an AI coding assistant.

## Phase 1: Commander (Quick Fix)

For quick ad-hoc merging.

```markdown
I have a folder `Sales_Reports` containing multiple Excel files (.xlsx, .xls). Write a robust Python script using Pandas to:

**Find Files:**
- Scan for all .xlsx and .xls files (skip temp files starting with ~$).

**Read Safely:**
- Use try-except to handle corrupted or locked files gracefully (skip with warning).

**Add Metadata:**
- Add columns `Source_File` (filename) and `Row_Index` (original row number).

**Merge:**
- Concatenate all DataFrames, reset index.

**Export:**
- Save to `Master_Report.xlsx` with openpyxl engine.

**Logging:**
- Print progress (e.g., 'Processing 1/50: sales_jan.xlsx').

Handle encoding issues (UTF-8) and empty files (skip with warning).
```

**Result:** A robust merge script that handles edge cases.

## Phase 2: Architect (Permanent Tool)

For regular reporting.

```markdown
**Role:** Python GUI Developer (PyQt6 Specialist)
**Task:** Create "Excel Merge Master" Desktop App

**Objective:** A reliable desktop tool to consolidate hundreds of Excel files into a single master report with traceability.

**Tech Stack:**
* Language: Python 3.10+
* GUI Library: PyQt6 (Cross-platform)
* Data Engine: Pandas, openpyxl
* Packaging: PyInstaller

**Functional Requirements:**
1.  **UI Layout (PyQt6):**
    *   **📂 Input Section:**
        *   "Browse Folder" button for source reports.
        *   Status label showing "Found X valid Excel files".
    *   **📤 Output Section:**
        *   "Browse Output Folder" button (optional, defaults to input folder).
        *   Output Filename field (default: Master_Report.xlsx).
    *   **⚙️ Settings Section:**
        *   Dropdown for "Encoding" (Auto/UTF-8/Latin-1/CP1252).
    *   **📊 Progress Section:**
        *   Progress bar and log display.
    *   **Action:** Big "🚀 Merge All Files" button.

2.  **Core Logic:**
    *   Scan folder for `.xlsx/.xls`, ignoring `~$` temp files.
    *   Add `Source_File` column to every row for traceability.
    *   Handle locked/corrupted files with try/except blocks (skip and log).
    *   **Threading:** File I/O operations in `QThread` to prevent freezing.

3.  **Deliverables:**
    *   `main.py`: Complete source code.
    *   `requirements.txt`: Dependencies (PyQt6, Pandas, openpyxl, pyinstaller).
    *   **Launcher Scripts (double-click to run):**
        *   Windows: `ExcelMerge.bat`
            ```batch
            @echo off
            cd /d "%~dp0"
            python main.py
            ```
        *   macOS: `ExcelMerge.command`
            ```bash
            #!/bin/bash
            cd "$(dirname "$0")"
            python3 main.py
            ```
            (Run `chmod +x ExcelMerge.command` first)
```

**Build Executable (optional, for distribution):**
*   Windows (.exe): `python -m PyInstaller --onefile --noconsole --name "ExcelMerge" main.py`
*   macOS (.app): `python -m PyInstaller --windowed --noconsole --name "ExcelMerge" main.py`
*   Output in `dist/` folder.
*   Note: Must build on target OS (Windows for .exe, macOS for .app).
