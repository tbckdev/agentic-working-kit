# Sample Data

This folder contains sample Excel files for testing the Excel Merge workflow.

## Structure

```
sample-data/
├── input/          # Place Excel files here (.xlsx, .xls)
└── output/         # Merged Master_Report.xlsx will be saved here
```

## Notes

- Place your Excel files (.xlsx, .xls) in the `input/` folder
- Temp files starting with ~$ will be automatically skipped
- Output folder will be created automatically
- Each row in output will have Source_File column indicating origin
