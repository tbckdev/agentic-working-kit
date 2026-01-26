"""
{{WORKFLOW_TITLE}} - Core Script
Description of what this script does.
"""

import json
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_data(config):
    """Main processing function."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load paths from config
    input_file = os.path.join(base_dir, config['input_file'])
    output_dir = os.path.join(base_dir, config['output_dir'])
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        else:
            df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
    
    # Process each row
    total = len(df)
    for index, row in df.iterrows():
        try:
            # TODO: Add your processing logic here
            item_name = str(row.iloc[0]).strip()
            
            # Example: Create output file
            output_path = os.path.join(output_dir, f"output-{index}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Processed: {item_name}")
            
            print(f"Processed {index + 1}/{total}: {item_name}")
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
    
    print(f"\nComplete! Output saved to: {output_dir}")


if __name__ == "__main__":
    config = load_config()
    process_data(config)
