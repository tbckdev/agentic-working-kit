---
description: Create personalized invitation cards from guest list and template image
---

# Invitation Maker

Batch create personalized invitation cards with guest names from an Excel file, placed onto a template image.

## Objective
- Create N invitation image files (1 file/guest)
- Guest name is placed at the correct position and font according to config

## Mandatory Configuration ⚠️

> **STOP AND CHECK** before performing any steps!
> If inputs are missing -> ASK user immediately. DO NOT assume.

| #   | Input          | Description                               | Example                                |
| --- | -------------- | ----------------------------------------- | -------------------------------------- |
| 1   | Template Image | PNG/JPG file as background                | `template.png`                         |
| 2   | Guest List     | Excel file (.xlsx), first column has name | `guests.xlsx`                          |
| 3   | Font           | Font name or .ttf path                    | `Roboto`, `C:/Windows/Fonts/arial.ttf` |

**Sample Questions:**
```
To generate invitations, I need the following information:
1. Path to the template image (PNG/JPG)?
2. Path to the Excel guest list file?
3. Font to use (font name or .ttf file)?
```

---

## Execution Steps

### Step 1: Check working directory
// turbo
```bash
ls -la
```

### Step 2: Find and Verify Font

**Priority 1 - System Font (Windows):**
// turbo
```powershell
Get-ChildItem "C:\Windows\Fonts" -Filter "*[FONT_NAME]*" -ErrorAction SilentlyContinue
```

**Priority 2 - Project Font:**
```bash
ls fonts/
```

**Priority 3 - Download from Google Fonts:**
```powershell
# Roboto
Invoke-WebRequest -Uri "https://github.com/googlefonts/roboto/releases/download/v2.138/roboto-unhinted.zip" -OutFile roboto.zip
Expand-Archive -Path roboto.zip -DestinationPath fonts -Force

# Be Vietnam Pro
Invoke-WebRequest -Uri "https://fonts.google.com/download?family=Be%20Vietnam%20Pro" -OutFile bevietnam.zip
Expand-Archive -Path bevietnam.zip -DestinationPath fonts -Force
```

### Step 3: Create/Update config.json

```json
{
    "input_excel": "guests.xlsx",
    "template_image": "template.png",
    "output_dir": "invitations",
    "font_settings": {
        "path": "C:/Windows/Fonts/arial.ttf",
        "size": 60,
        "color": [255, 165, 0]
    },
    "text_position": {
        "y": 330,
        "center_x": 600
    }
}
```

### Step 4: Configure Text Position (Optional)

```bash
python web_server.py
```
Open `http://localhost:8000`, drag and drop text, click Save.

### Step 5: Generate Invitations
// turbo
```bash
python generate_invitations.py
```

### Step 6: Verify Results
// turbo
```bash
ls invitations/
```

---

## Expected Output
- Directory `invitations/` contains N PNG files
- Each file format: `invitation-[Guest Name].png`

## Quick Reference

### Available Windows Fonts
| Font            | Path                           |
| --------------- | ------------------------------ |
| Arial           | `C:/Windows/Fonts/arial.ttf`   |
| Arial Bold      | `C:/Windows/Fonts/arialbd.ttf` |
| Times New Roman | `C:/Windows/Fonts/times.ttf`   |
| Segoe UI        | `C:/Windows/Fonts/segoeui.ttf` |
| Tahoma          | `C:/Windows/Fonts/tahoma.ttf`  |

### Common Colors (RGB)
| Color  | RGB               |
| ------ | ----------------- |
| White  | `[255, 255, 255]` |
| Gold   | `[255, 215, 0]`   |
| Orange | `[255, 165, 0]`   |
| Red    | `[255, 0, 0]`     |

## Error Handling / Edge Cases

| Scenario                        | Resolution                               |
| ------------------------------- | ---------------------------------------- |
| Font doesn't support Vietnamese | Switch to Arial or Roboto                |
| Excel missing "Name" column     | Use the first column                     |
| Font not found                  | Download from Google Fonts or use system |
| Guest name too long             | Reduce `font_size` in config             |
