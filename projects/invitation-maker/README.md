# Invitation Maker Project

Bulk generate personalized invitation cards from Excel data with QR code support.

## 🚀 Overview

This tool automates the process of creating hundreds of personalized invitations. It takes an Excel file (guest list) and a base invitation image, then overlays text (Name, Table No) and QR codes onto each image automatically.

## ✨ Features

- **Bulk Processing**: Generate 1000+ invitations in seconds.
- **Excel/CSV Support**: Import guest data easily.
- **Custom Fonts**: Support for `.ttf` and `.otf` fonts.
- **QR Code Generation**: Auto-generate QR codes from text/links in Excel.
- **Smart Positioning**: Drag & drop text/QR code on the GUI preview.
- **Color Customization**: Pick exact colors for text.

## 🛠️ Usage

### Quick Start (GUI)

1. **Window/Mac**: Download the latest release from [Releases](https://github.com/egany/agentic-working-kit/releases).
2. Run `InvitationMaker.exe`.
3. **Step 1**: Load your Guest List (Excel file).
4. **Step 2**: Load your Template Image (.jpg, .png).
5. **Step 3**: Configure Layout
   - Drag "Guest Name" to position.
   - Drag "QR Code" to position.
   - Adjust Font, Size, Color.
6. **Step 4**: Click **Start Generate**.

### Developer Mode (Scripts)

Run the Python script directly:

```bash
cd scripts
pip install -r requirements.txt
python generate_invitations.py
```

## 📋 Requirements

- Input Excel file columns: `Guest Name`, `QR Data` (optional), `Table` (optional).
- Template Image: High-resolution PNG/JPG.
- Fonts: Custom fonts must be installed or provided in path.

## 📂 Project Structure

```text
projects/invitation-maker/
├── tools/              # GUI Application (PyQt6)
├── scripts/            # Core logic script
├── workflows/          # AI execution guide
└── sample-data/        # Example inputs & outputs
```
