---
name: python-packaging
description: Guide for packaging Python apps with PyInstaller for Windows and macOS
---

# Python Packaging Skill

Hướng dẫn đóng gói ứng dụng Python thành file thực thi (.exe, .app) chuyên nghiệp với PyInstaller.

## 📦 PyInstaller Basics

### Cài đặt
```bash
pip install pyinstaller
```

### Lệnh cơ bản
| Flag              | Ý nghĩa                                                  |
| ----------------- | -------------------------------------------------------- |
| `--onefile`       | Gộp tất cả vào 1 file duy nhất (tốt cho tools nhỏ)       |
| `--onedir`        | Giữ nguyên folder (tốt cho app lớn, khởi động nhanh hơn) |
| `--windowed`      | Ẩn console window (GUI apps)                             |
| `--noconsole`     | Giống `--windowed`                                       |
| `--name "App"`    | Đặt tên file output                                      |
| `--icon=icon.ico` | Đặt icon (Windows: .ico, Mac: .icns)                     |

---

## 🪟 Windows Packaging

### Command chuẩn cho GUI App
```bash
python -m PyInstaller --onefile --noconsole --name "MyApp" main.py
```

### Command chuẩn cho Console Tool
```bash
python -m PyInstaller --onefile --name "MyTool" main.py
```

### ⚠️ Lưu ý Windows
- Windows Defender có thể báo False Positive với `--onefile`. Dùng `--onedir` nếu cần tránh.
- Icon bắt buộc file `.ico`.

---

## 🍎 macOS Packaging

### Command chuẩn
```bash
python -m PyInstaller --windowed --noconsole --name "MyApp" main.py
```

### ⚠️ Lưu ý macOS
- Không hỗ trợ `--onefile` tốt như Windows (khởi động rất chậm). Nên dùng mặc định (`--onedir`) hoặc `--windowed`.
- Kết quả là `.app` bundle, không phải 1 file.
- Cần sign code nếu muốn chạy trên máy khác mà không bị chặn Security (nâng cao).

---

## 🛠️ Handling Assets (Images, Configs)

Khi đóng gói `--onefile`, assets bị nén vào thư mục tạm `_MEIxxxx`. Cần code để tìm đúng đường dẫn:

### Pattern: Resource Path
```python
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Sử dụng
icon_path = resource_path("icon.png")
```

### Thêm assets vào build
Sử dụng flag `--add-data`:
- **Windows**: `--add-data "src;dest"`
- **macOS/Linux**: `--add-data "src:dest"`

Ví dụ:
```bash
# Windows
pyinstaller --onefile --add-data "config.json;." main.py
```

---

## 📄 requirements.txt Best Practices

Luôn tối ưu file `requirements.txt` trước khi build để giảm dung lượng file exe.

### Không nên:
`pip freeze > requirements.txt` (Lấy cả những lLibrary rác hệ thống)

### Nên:
Chỉ liệt kê library thực sự dùng:
```text
PyQt6>=6.4.0
pandas
openpyxl
pillow
```

---

## 🤖 Cross-Platform Rules

**PyInstaller không phải là Cross-Compiler.**
- Muốn file `.exe` -> Phải build trên Windows.
- Muốn file `.app` -> Phải build trên macOS.

**Giải pháp:**
1. Dùng CI/CD (GitHub Actions) để build cả 2.
2. Hoặc setup máy ảo (VM) để build.

---

## ✅ Packaging Checklist
- [ ] Run `pip install -r requirements.txt` trước
- [ ] Test app chạy ok bằng `python main.py` chưa
- [ ] Xử lý đường dẫn assets (`resource_path`)
- [ ] Chạy lệnh build đúng OS
- [ ] Test file output trong thư mục `dist/`
- [ ] Kiểm tra virus scan (cho Windows)
