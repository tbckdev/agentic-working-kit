---
description: Merge multiple Excel files into a single master report with traceability
---

# Excel Merge

Consolidate multiple Excel files into one master report with Source_File column for traceability.

## Objective
- Merge all .xlsx/.xls files from a folder
- Add Source_File column to track origin
- Handle corrupted/locked files gracefully

## Mandatory Configuration ⚠️

> **STOP AND CHECK** before performing any steps!
> If inputs are missing -> ASK user immediately. DO NOT assume.

| #   | Input        | Description                   | Example              |
| --- | ------------ | ----------------------------- | -------------------- |
| 1   | Input Folder | Folder containing Excel files | `Sales_Reports/`     |
| 2   | Output File  | Name of merged output file    | `Master_Report.xlsx` |
| 3   | Encoding     | File encoding (optional)      | `UTF-8` or `Auto`    |

**Sample Questions:**
```
To merge Excel files, I need the following information:
1. Path to the folder containing Excel files?
2. Output filename for the merged report?
3. Encoding preference (Auto/UTF-8)?
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
```

### Step 3: Create/Update config.json

```json
{
    "input_dir": "../sample-data/input",
    "output_file": "../sample-data/output/Master_Report.xlsx",
    "encoding": "utf-8",
    "skip_temp_files": true,
    "add_source_column": true
}
```

### Step 4: Run the merger
// turbo
```bash
python excel_merge.py
```

### Step 5: Verify results
// turbo
```bash
ls output/
```

---

## Expected Output
- Single `Master_Report.xlsx` containing all rows from all files
- `Source_File` column indicating origin of each row
- `Row_Index` column showing original row number

## Quick Reference

### Common Settings
| Setting           | Description                 | Default |
| ----------------- | --------------------------- | ------- |
| skip_temp_files   | Skip files starting with ~$ | true    |
| add_source_column | Add Source_File column      | true    |
| encoding          | File encoding               | utf-8   |

## Error Handling / Edge Cases

| Scenario             | Resolution                             |
| -------------------- | -------------------------------------- |
| File is locked       | Skip with warning, continue processing |
| Corrupted file       | Skip with warning, continue processing |
| Empty file           | Skip with warning                      |
| No Excel files found | Show error message                     |
| Encoding error       | Try fallback encoding                  |
