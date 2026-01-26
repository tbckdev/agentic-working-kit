import json
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def load_config(config_path='config.json'):
    # Resolve config path relative to this script file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_invitations():
    config = load_config()
    
    # Paths (relative to script execution or absolute)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_excel = os.path.join(base_dir, config['input_excel'])
    template_path = os.path.join(base_dir, config['template_image'])
    output_dir = os.path.join(base_dir, config['output_dir'])
    font_path = os.path.join(base_dir, config['font_settings']['path'])
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load Data
    try:
        df = pd.read_excel(input_excel)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Check for Name column
    name_col = 'Name'
    if name_col not in df.columns:
        name_col = df.columns[0] # Fallback to first column
        print(f"Column 'Name' not found, using first column: '{name_col}'")
    
    # Load Template to get size
    try:
        template = Image.open(template_path)
        img_w, img_h = template.size
    except Exception as e:
        print(f"Error loading template: {e}")
        return

    # Load Font
    font_size = config['font_settings'].get('size', 60)
    font_color = tuple(config['font_settings'].get('color', [0, 0, 0]))
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font not found at {font_path}, falling back to default.")
        font = ImageFont.load_default()

    # Process each guest
    for index, row in df.iterrows():
        guest_name = str(row[name_col]).strip()
        if not guest_name or guest_name.lower() == 'nan':
            continue
            
        # Create valid filename
        safe_name = "".join([c for c in guest_name if c.isalpha() or c.isdigit() or c==' ']).strip()
        filename = f"invitation-{safe_name}.png"
        output_path = os.path.join(output_dir, filename)
        
        # New image copy
        img = template.copy()
        draw = ImageDraw.Draw(img)
        
        # Calculate Text Position
        # using textbbox for better accuracy in Pillow >= 9.2.0
        # fallback to textsize if older (though textsize is deprecated)
        try:
            left, top, right, bottom = draw.textbbox((0, 0), guest_name, font=font)
            text_width = right - left
            text_height = bottom - top
        except AttributeError:
             text_width, text_height = draw.textsize(guest_name, font=font)

        y_pos = config['text_position']['y']
        
        if config['text_position']['center_x'] == 'center':
            x_pos = (img_w - text_width) // 2
        else:
            x_pos = int(config['text_position']['center_x']) - (text_width // 2) # Assuming center_x means the center point
            
        # Draw Text
        draw.text((x_pos, y_pos), guest_name, font=font, fill=font_color)
        
        # Save
        img.save(output_path)
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_invitations()
