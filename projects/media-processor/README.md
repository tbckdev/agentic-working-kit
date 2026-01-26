# Media Processor

Smart Image Processor for e-commerce: standardizes product images to uniform size with watermark overlay.

## Features

- **Smart Padding**: Adds white borders instead of cropping, preserving the whole product
- **Auto-Scaling**: Resizes watermark so it never covers the product
- **Batch Processing**: Handles thousands of images with progress bar and ETA
- **Error Handling**: Skips corrupt images with warnings instead of crashing

## Requirements

- Python 3.10+
- Dependencies listed in `scripts/requirements.txt`

## Quick Start

### Option 1: Run Script Directly
```bash
cd scripts
pip install -r requirements.txt
python media_processor.py
```

### Option 2: Use GUI Tool
```bash
cd tools
pip install -r requirements.txt
# Windows: double-click MediaProcessor.bat
# macOS: double-click MediaProcessor.command
```

### Option 3: Use AI Agent
Follow the prompts in `prompt-guide.md` or use the workflow in `workflows/media-processor.md`.

## Configuration

Edit `scripts/config.json` to customize:
- Canvas size (default: 1000x1000)
- Watermark settings (opacity, max width %)
- Output quality

## Sample Data

The `sample-data/` folder contains example files for testing:
- `input/` - Sample product images
- `watermark.png` - Sample watermark
- `output/` - Generated output files

## License

MIT License
