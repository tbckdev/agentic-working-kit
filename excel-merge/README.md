# Excel Merge Master

Consolidate multiple Excel files into a single master report with traceability.

## Features

- **Traceability**: Adds Source_File column so you know which row came from which file
- **Smart Skip**: Ignores temporary files (~$temp.xlsx) and handles locked/corrupt files gracefully
- **Encoding Support**: Handles UTF-8 and other encodings automatically
- **Error Handling**: Skip corrupted files with warnings instead of crashing

## Requirements

- Python 3.10+
- Dependencies listed in `scripts/requirements.txt`

## Quick Start

### Option 1: Run Script Directly
```bash
cd scripts
pip install -r requirements.txt
python excel_merge.py
```

### Option 2: Use GUI Tool
```bash
cd tools
pip install -r requirements.txt
# Windows: double-click ExcelMerge.bat
# macOS: double-click ExcelMerge.command
```

### Option 3: Use AI Agent
Follow the prompts in `prompt-guide.md` or use the workflow in `workflows/excel-merge.md`.

## Configuration

Edit `scripts/config.json` to customize:
- Input folder path
- Output filename
- Encoding settings

## Sample Data

The `sample-data/` folder contains example files for testing:
- `input/` - Sample Excel files to merge
- `output/` - Generated master report

## License

MIT License
