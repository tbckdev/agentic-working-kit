"""
Media Processor - Smart Image Processor for E-commerce
Standardizes product images to uniform size with watermark overlay.
"""

import json
import os
from PIL import Image, ImageOps


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def smart_resize(img, canvas_size, bg_color):
    """Resize image to fit canvas with padding, maintaining aspect ratio."""
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'P'):
        background = Image.new('RGB', img.size, bg_color)
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Use ImageOps.pad for smart resize with padding
    result = ImageOps.pad(img, (canvas_size, canvas_size), color=tuple(bg_color))
    return result


def apply_watermark(img, watermark_path, settings):
    """Apply watermark to image with auto-scaling and opacity."""
    try:
        watermark = Image.open(watermark_path).convert('RGBA')
    except Exception as e:
        print(f"Warning: Could not load watermark: {e}")
        return img
    
    img_width, img_height = img.size
    wm_width, wm_height = watermark.size
    
    # Auto-scale watermark if too large
    max_width = int(img_width * settings['max_width_percent'] / 100)
    if wm_width > max_width:
        ratio = max_width / wm_width
        new_size = (int(wm_width * ratio), int(wm_height * ratio))
        watermark = watermark.resize(new_size, Image.Resampling.LANCZOS)
        wm_width, wm_height = watermark.size
    
    # Apply opacity
    opacity = settings.get('opacity', 0.5)
    alpha = watermark.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    watermark.putalpha(alpha)
    
    # Calculate position
    position = settings.get('position', 'center')
    if position == 'center':
        x = (img_width - wm_width) // 2
        y = (img_height - wm_height) // 2
    elif position == 'bottom-right':
        x = img_width - wm_width - 20
        y = img_height - wm_height - 20
    elif position == 'bottom-left':
        x = 20
        y = img_height - wm_height - 20
    else:
        x = (img_width - wm_width) // 2
        y = (img_height - wm_height) // 2
    
    # Paste watermark
    img_rgba = img.convert('RGBA')
    img_rgba.paste(watermark, (x, y), watermark)
    return img_rgba.convert('RGB')


def process_images(config):
    """Main processing function."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_dir = os.path.join(base_dir, config['input_dir'])
    output_dir = os.path.join(base_dir, config['output_dir'])
    watermark_path = os.path.join(base_dir, config['watermark_path'])
    
    canvas_size = config.get('canvas_size', 1000)
    bg_color = config.get('background_color', [255, 255, 255])
    wm_settings = config.get('watermark_settings', {})
    quality = config.get('output_quality', 90)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of images
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')
    images = [f for f in os.listdir(input_dir) 
              if f.lower().endswith(supported_formats)]
    
    if not images:
        print(f"No images found in {input_dir}")
        return
    
    total = len(images)
    processed = 0
    errors = 0
    
    for i, filename in enumerate(images, 1):
        input_path = os.path.join(input_dir, filename)
        output_filename = os.path.splitext(filename)[0] + '.jpg'
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            # Load image
            img = Image.open(input_path)
            
            # Smart resize
            img = smart_resize(img, canvas_size, bg_color)
            
            # Apply watermark
            if os.path.exists(watermark_path):
                img = apply_watermark(img, watermark_path, wm_settings)
            
            # Save
            img.save(output_path, 'JPEG', quality=quality)
            processed += 1
            print(f"Processed {i}/{total}: {filename}")
            
        except Exception as e:
            errors += 1
            print(f"Warning: Skipped {filename} - {e}")
            continue
    
    print(f"\nComplete! Processed: {processed}, Errors: {errors}")
    print(f"Output saved to: {output_dir}")


if __name__ == "__main__":
    config = load_config()
    process_images(config)
