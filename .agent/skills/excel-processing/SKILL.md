---
name: excel-processing
description: Best practices for robust Excel data processing with Pandas and OpenPyXL
---

# Excel Processing Skill

Guide for efficient, safe, and standards-compliant Excel data processing.

## 📖 Reading Excel Files

### 1. Engine Selection
Always determine the appropriate engine:
- `.xlsx`: Use `openpyxl` (Default modern format).
- `.xls`: Use `xlrd` (Legacy format).
- `.csv`: Use `pandas.read_csv`.

### 2. Robust Reading Pattern
```python
def read_excel_safe(filepath):
    try:
        if filepath.lower().endswith('.xlsx'):
            return pd.read_csv(filepath, engine='openpyxl')
        elif filepath.lower().endswith('.xls'):
            return pd.read_csv(filepath, engine='xlrd')
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    ```

### 3. Handling Temp Files
Always skip Excel temp files (`~$filename.xlsx`):
```python
if filename.startswith('~$'):
    continue
```

---

## 💾 Writing Excel Files

### 1. Preserving Data
Use `index=False` unless index has meaning:
```python
df.to_excel("output.xlsx", index=False, engine='openpyxl')
```

### 2. Large Data Sets
For large datasets (>100k rows), `openpyxl` can be slow. Consider:
- Splitting into multiple files.
- Using CSV if formatting is not needed.

---

## 🛡️ Error Handling Patterns

### 1. File Locking
Excel file open by user will be locked.
**Solution:** Catch `PermissionError`.

```python
try:
    df.to_excel("output.xlsx")
except PermissionError:
    print("Error: File is open. Please close Excel and try again.")
```

### 2. Corrupted Files
File downloaded from internet or corrupted format.
**Solution:** Catch `BadZipFile` or `ValueError`.

### 3. Encoding (CSV)
CSV might have encoding issues (e.g. non-ASCII characters).
**Solution:** Try list of common encodings.
```python
encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin1']
for enc in encodings:
    try:
        return pd.read_csv(file, encoding=enc)
    except:
        continue
```

---

## 🔎 Data Validation

### Check Empty
```python
if df.empty:
    print("File has no data")
    return
```

### Check Columns
Ensure input file has required columns:
```python
required = ['Name', 'Email']
if not all(col in df.columns for col in required):
    print("Missing required columns")
```

---

## 🚀 Performance Tips

1.  **Read specific columns**: `pd.read_excel(..., usecols=['A', 'B'])` to reduce RAM usage.
2.  **Specify dtypes**: `dtype={'Phone': str}` to avoid losing leading zeros.
3.  **Process chunking**: For huge files (GB), read by chunk (mostly with CSV).

---

## ✅ Checklist
- [ ] Select correct engine (`openpyxl` vs `xlrd`)
- [ ] Skip temp files `~$`
- [ ] Handle `PermissionError` (File locked)
- [ ] Handle `UnicodeDecodeError` (Encoding)
- [ ] Check `df.empty` before processing
