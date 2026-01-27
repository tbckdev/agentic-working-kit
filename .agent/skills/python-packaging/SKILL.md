---
name: python-packaging
description: Guide for packaging Python apps with PyInstaller for Windows and macOS
---

# Python Packaging Skill

Guide for packaging Python applications into professional executable files (.exe, .app) using PyInstaller.

## 📦 PyInstaller Basics

### Installation
```bash
pip install pyinstaller
```

### Basic Commands
| Flag              | Meaning                                                     |
| ----------------- | ----------------------------------------------------------- |
| `--onefile`       | Bundle everything into a single file (good for small tools) |
| `--onedir`        | Keep folder structure (good for large apps, faster startup) |
| `--windowed`      | Hide console window (GUI apps)                              |
| `--noconsole`     | Same as `--windowed`                                        |
| `--name "App"`    | Set output filename                                         |
| `--icon=icon.ico` | Set icon (Windows: .ico, Mac: .icns)                        |

---

## 🪟 Windows Packaging

### Standard Command for GUI App
```bash
python -m PyInstaller --onefile --noconsole --name "MyApp" main.py
```

### Standard Command for Console Tool
```bash
python -m PyInstaller --onefile --name "MyTool" main.py
```

### ⚠️ Windows Notes
- Windows Defender might report False Positive with `--onefile`. Use `--onedir` if avoiding this is priority.
- Icon must be `.ico` file.

---

## 🍎 macOS Packaging

### Standard Command
```bash
python -m PyInstaller --windowed --noconsole --name "MyApp" main.py
```

### ⚠️ macOS Notes
- Does not support `--onefile` very well (slow startup). Recommend default (`--onedir`) or `--windowed`.
- Result is `.app` bundle, not a single file.
- Needs code signing if running on other machines to avoid Security blocks (advanced).

---

## 🛠️ Handling Assets (Images, Configs)

When packaging with `--onefile`, assets are unpacked to a temp folder `_MEIxxxx`. Code is needed to find the correct path:

### Pattern: Resource Path
```python
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Usage
icon_path = resource_path("icon.png")
```

### Adding assets to build
Use `--add-data` flag:
- **Windows**: `--add-data "src;dest"`
- **macOS/Linux**: `--add-data "src:dest"`

Example:
```bash
# Windows
pyinstaller --onefile --add-data "config.json;." main.py
```

---

## 📄 requirements.txt Best Practices

Always optimize `requirements.txt` before building to reduce exe size.

### Do NOT:
`pip freeze > requirements.txt` (Captures all system junk libraries)

### DO:
List only actually used libraries:
```text
PyQt6>=6.4.0
pandas
openpyxl
pillow
```

---

## 🤖 Cross-Platform Rules

**PyInstaller is NOT a Cross-Compiler.**
- Want `.exe` file -> Must build on Windows.
- Want `.app` file -> Must build on macOS.

**Solutions:**
1. Use CI/CD (GitHub Actions) to build both.
2. Or setup Virtual Machine (VM) to build.

---

## ✅ Packaging Checklist
- [ ] Run `pip install -r requirements.txt` first
- [ ] Test app runs okay with `python main.py`
- [ ] Handle asset paths (`resource_path`)
- [ ] Run correct build command for OS
- [ ] Test output file in `dist/` directory
- [ ] Check virus scan (for Windows)

---

## 🤖 Agentic Protocol

### Skill Metadata
- **Version**: 1.0.0
- **Last Updated**: 2026-01-27

### 1. Activation Log
When activating this skill, print:
"🎯 [SKILL ACTIVATED] python-packaging v1.0.0"
"📋 Parameters:"
"   - Target: [script.py]"
"   - Mode: [onefile|onedir]"
"   - OS: [Windows|macOS]"
"   - Assets: [list_of_included_assets]"

### 2. User Confirmation
Before running the build command (long process):
"I'm about to package [Target] using PyInstaller with options: [Options]. This may take a few minutes. Proceed?"

### 3. Completion Log
- Success: "✅ [python-packaging] Build complete. Artifact: dist/[filename]"
- Error: "❌ [python-packaging] Build failed. Check logs."

