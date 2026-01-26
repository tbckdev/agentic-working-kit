---
description: Batch process product images with smart resize and watermark overlay
---

# Media Processor

Standardize e-commerce product images to uniform 1000x1000 size with watermark overlay.

## Objective
- Resize images to 1000x1000 with white padding (no cropping)
- Apply watermark with auto-scaling and opacity
- Batch process hundreds/thousands of images

## Mandatory Configuration ⚠️

> **STOP AND CHECK** before performing any steps!
> If inputs are missing -> ASK user immediately. DO NOT assume.

| #   | Input         | Description                      | Example         |
| --- | ------------- | -------------------------------- | --------------- |
| 1   | Input Folder  | Folder containing product images | `input/`        |
| 2   | Watermark     | PNG file with transparency       | `watermark.png` |
| 3   | Output Folder | Where to save processed images   | `output/`       |

**Sample Questions:**
```
To process images, I need the following information:
1. Path to the folder containing product images?
2. Path to the watermark PNG file?
3. Output folder for processed images?
```

---

## Execution Steps

### Step 1: Check working directory
// turbo
```bash
ls -la
```

### Step 2: Verify input files exist
// turbo
```bash
ls input/
ls watermark.png
```

### Step 3: Create/Update config.json

```json
{
    "input_dir": "input",
    "output_dir": "output",
    "watermark_path": "watermark.png",
    "canvas_size": 1000,
    "background_color": [255, 255, 255],
    "watermark_settings": {
        "max_width_percent": 30,
        "opacity": 0.5,
        "position": "center"
    },
    "output_quality": 90
}
```

### Step 4: Run the processor
// turbo
```bash
python media_processor.py
```

### Step 5: Verify results
// turbo
```bash
ls output/
```

---

## Expected Output
- All images resized to 1000x1000 with white padding
- Watermark applied at center with 50% opacity
- Output as JPG files in `output/` folder

## Quick Reference

### Common Settings
| Setting           | Description                  | Default |
| ----------------- | ---------------------------- | ------- |
| canvas_size       | Output image size (square)   | 1000    |
| max_width_percent | Max watermark width %        | 30      |
| opacity           | Watermark transparency (0-1) | 0.5     |
| output_quality    | JPG quality (1-100)          | 90      |

### Watermark Positions
| Position     | Description         |
| ------------ | ------------------- |
| center       | Center of image     |
| bottom-right | Bottom right corner |
| bottom-left  | Bottom left corner  |

## Error Handling / Edge Cases

| Scenario            | Resolution                             |
| ------------------- | -------------------------------------- |
| Corrupt image file  | Skip with warning, continue processing |
| RGBA image          | Convert to RGB before saving as JPG    |
| Watermark too large | Auto-scale to max 30% width            |
| No images in folder | Show error message                     |
