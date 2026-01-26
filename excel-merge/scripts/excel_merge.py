"""
Excel Merge Master - Core Script
Consolidate multiple Excel files into a single master report with traceability.
"""

import json
import os
import pandas as pd


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_excel_files(input_dir, skip_temp=True):
    """Find all Excel files in directory, optionally skipping temp files."""
    excel_extensions = ('.xlsx', '.xls')
    files = []
    
    for f in os.listdir(input_dir):
        if f.lower().endswith(excel_extensions):
            # Skip temp files (starting with ~$)
            if skip_temp and f.startswith('~$'):
                print(f"Skipping temp file: {f}")
                continue
            files.append(os.path.join(input_dir, f))
    
    return files


def read_excel_safe(filepath, encoding='utf-8'):
    """Read Excel file with error handling."""
    try:
        # Try reading with openpyxl first (for .xlsx)
        if filepath.lower().endswith('.xlsx'):
            df = pd.read_excel(filepath, engine='openpyxl')
        else:
            # Use xlrd for .xls files
            df = pd.read_excel(filepath, engine='xlrd')
        return df
    except Exception as e:
        print(f"Warning: Could not read {os.path.basename(filepath)}: {e}")
        return None


def merge_excel_files(config):
    """Main function to merge Excel files."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_dir = os.path.join(base_dir, config['input_dir'])
    output_file = os.path.join(base_dir, config['output_file'])
    skip_temp = config.get('skip_temp_files', True)
    add_source = config.get('add_source_column', True)
    add_row_index = config.get('add_row_index', True)
    encoding = config.get('encoding', 'utf-8')
    
    # Find Excel files
    files = find_excel_files(input_dir, skip_temp)
    
    if not files:
        print(f"No Excel files found in {input_dir}")
        return
    
    print(f"Found {len(files)} Excel files to merge")
    
    # Merge all files
    all_dfs = []
    processed = 0
    skipped = 0
    
    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        print(f"Processing {i}/{len(files)}: {filename}")
        
        df = read_excel_safe(filepath, encoding)
        
        if df is None:
            skipped += 1
            continue
            
        if df.empty:
            print(f"Warning: {filename} is empty, skipping")
            skipped += 1
            continue
        
        # Add metadata columns
        if add_source:
            df['Source_File'] = filename
        
        if add_row_index:
            df['Row_Index'] = range(1, len(df) + 1)
        
        all_dfs.append(df)
        processed += 1
    
    if not all_dfs:
        print("No data to merge!")
        return
    
    # Concatenate all DataFrames
    print("\nMerging all files...")
    master_df = pd.concat(all_dfs, ignore_index=True)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save to Excel
    master_df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"\n✅ Complete!")
    print(f"   Processed: {processed} files")
    print(f"   Skipped: {skipped} files")
    print(f"   Total rows: {len(master_df)}")
    print(f"   Output: {output_file}")


if __name__ == "__main__":
    config = load_config()
    merge_excel_files(config)
