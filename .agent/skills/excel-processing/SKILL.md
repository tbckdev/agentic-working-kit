---
name: excel-processing
description: Best practices for robust Excel data processing with Pandas and OpenPyXL
---

# Excel Processing Skill

Hướng dẫn xử lý file Excel hiệu quả, an toàn và đúng chuẩn dữ liệu.

## 📖 Reading Excel Files

### 1. Engine Selection
Luôn xác định engine phù hợp:
- `.xlsx`: Dùng `openpyxl` (Default modern format).
- `.xls`: Dùng `xlrd` (Legacy format).
- `.csv`: Dùng `pandas.read_csv`.

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
Luôn bỏ qua file tạm của Excel (`~$filename.xlsx`):
```python
if filename.startswith('~$'):
    continue
```

---

## 💾 Writing Excel Files

### 1. Preserving Data
Sử dụng `index=False` trừ khi index thực sự có ý nghĩa:
```python
df.to_excel("output.xlsx", index=False, engine='openpyxl')
```

### 2. Large Data Sets
Với dữ liệu lớn (>100k rows), `openpyxl` có thể chậm. Cân nhắc:
- Split thành nhiều file.
- Dùng CSV nếu không cần format.

---

## 🛡️ Error Handling Patterns

### 1. File Locking
File Excel đang mở bởi user sẽ bị khóa.
**Giải pháp:** Catch `PermissionError`.

```python
try:
    df.to_excel("output.xlsx")
except PermissionError:
    print("Error: File is open. Please close Excel and try again.")
```

### 2. Corrupted Files
File tải từ mạng về hoặc bị lỗi format.
**Giải pháp:** Catch `BadZipFile` hoặc `ValueError`.

### 3. Encoding (CSV)
CSV có thể lỗi font Tiếng Việt.
**Giải pháp:** Thử list encodings phổ biến.
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
Đảm bảo file input có đủ cột cần thiết:
```python
required = ['Name', 'Email']
if not all(col in df.columns for col in required):
    print("Missing required columns")
```

---

## 🚀 Performance Tips

1.  **Read specific columns**: `pd.read_excel(..., usecols=['A', 'B'])` để giảm RAM.
2.  **Specify dtypes**: `dtype={'Phone': str}` để tránh mất số 0 đầu.
3.  **Process chunking**: Với file cực lớn (GB), đọc từng chunk (chủ yếu với CSV).

---

## ✅ Checklist
- [ ] Chọn đúng engine (`openpyxl` vs `xlrd`)
- [ ] Bỏ qua file tạm `~$`
- [ ] Handle `PermissionError` (File locked)
- [ ] Handle `UnicodeDecodeError` (Encoding)
- [ ] Kiểm tra `df.empty` trước khi xử lý
