---
description: {{WORKFLOW_DESCRIPTION}}
---

# {{WORKFLOW_NAME}}

{{WORKFLOW_SUMMARY}}

## Objective
- Goal 1
- Goal 2

## Mandatory Configuration ⚠️

> **STOP AND CHECK** before performing any steps!
> If inputs are missing -> ASK user immediately. DO NOT assume.

| #   | Input      | Description               | Example        |
| --- | ---------- | ------------------------- | -------------- |
| 1   | Input File | Description of input file | `input.xlsx`   |
| 2   | Template   | Description of template   | `template.png` |
| 3   | Settings   | Description of settings   | `config.json`  |

**Sample Questions:**
```
To run this workflow, I need the following information:
1. Path to the input file?
2. Path to the template (if applicable)?
3. Any specific settings or preferences?
```

---

## Execution Steps

### Step 1: Check working directory
// turbo
```bash
ls -la
```

### Step 2: Verify input files
// turbo
```bash
ls input/
```

### Step 3: Update config.json

```json
{
    "input_file": "input.xlsx",
    "output_dir": "output",
    "settings": {
        "option1": "value1",
        "option2": "value2"
    }
}
```

### Step 4: Run the script
// turbo
```bash
python main_script.py
```

### Step 5: Verify results
// turbo
```bash
ls output/
```

---

## Expected Output
- Description of expected output files
- Output format and naming convention

## Quick Reference

### Common Settings
| Setting | Description | Default |
| ------- | ----------- | ------- |
| option1 | Description | value1  |
| option2 | Description | value2  |

## Error Handling / Edge Cases

| Scenario         | Resolution                 |
| ---------------- | -------------------------- |
| File not found   | Check path and try again   |
| Invalid format   | Ensure correct file format |
| Processing error | Check logs for details     |
