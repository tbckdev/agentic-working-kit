---
name: pyqt6-patterns
description: Best practices and patterns for building robust PyQt6 desktop applications
---

# PyQt6 Patterns Skill

Hướng dẫn xây dựng ứng dụng Desktop với PyQt6, tập trung vào kiến trúc, threading, và trải nghiệm người dùng.

## 🏗️ Architecture Pattern

Sử dụng mô hình tách biệt UI và Logic:

1.  **MainWindow**: Quản lý UI, Layout, Signals.
2.  **Worker Thread (QThread)**: Xử lý long-running tasks (IO, Network, Heavy computation).
3.  **Core Logic**: Functions thuần Python, độc lập với GUI.

### Ví dụ cấu trúc `main.py`
```python
# Imports
from PyQt6.QtWidgets import ...
from PyQt6.QtCore import QThread, pyqtSignal

# 1. Background Thread Class
class WorkerThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def run(self):
        try:
            # Heavy task here
            pass
        except Exception as e:
            self.error.emit(str(e))

# 2. Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def start_task(self):
        self.thread = WorkerThread(...)
        self.thread.progress.connect(self.on_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()
```

---

## 🧵 Threading (Critical)

**Quy tắc bất di bất dịch:** KHÔNG BAO GIỜ chạy heavy task trên Main Thread.

### Tại sao?
- Chặn Main Thread -> UI bị đơ (Not Responsings).
- Trên macOS: Gây hiện tượng "Beachball of death".

### Pattern chuẩn
Sử dụng `QThread`:
1. Tạo class kế thừa `QThread`.
2. Định nghĩa Signals (`pyqtSignal`) để giao tiếp ngược lại Main Thread.
3. Override hàm `run()`.
4. Khởi tạo và giữ reference đến thread (`self.thread`) trong MainWindow.
5. Kết nối signals và gọi `start()`.

---

## 🎨 UI & Layouts

### Layout Hierarchy
Luôn sử dụng Layouts để UI responsive:
```
QMainWindow
└── CentralWidget (QWidget)
    └── QVBoxLayout
        ├── QGroupBox ("Input")
        │   └── QFormLayout
        ├── QGroupBox ("Settings")
        │   └── QVBoxLayout
        └── QGroupBox ("Actions")
            └── QHBoxLayout
```

### Styles
Sử dụng Fusion style cho clean look cross-platform:
```python
app = QApplication(sys.argv)
app.setStyle("Fusion")
```

---

## ⚠️ Error Handling

### Pattern: Try-Except-Signal
Trong Worker Thread, luông dùng try-except và emit signal error:

```python
def run(self):
    try:
        # Dangerous code
        do_work()
    except Exception as e:
        self.error.emit(str(e)) # Gửi lỗi về UI
```

Trong UI, lắng nghe signal và hiển thị MessageBox:
```python
def on_error(self, message):
    self.btn_start.setEnabled(True) # Re-enable UI
    QMessageBox.critical(self, "Error", message)
```

---

## 📝 Widget Common Patterns

### File Booking
```python
path = QFileDialog.getExistingDirectory(self, "Select Folder")
if path:
    self.input_dir = path
    self.label.setText(path)
```

### Progress Bar
- **Unknown duration**: `progressBar.setRange(0, 0)`
- **Known duration**: `emit(percent)` từ thread -> `progressBar.setValue(percent)`

### Logs Display
Sử dụng `QTextEdit` readonly để hiển thị logs realtime:
```python
self.log_text = QTextEdit()
self.log_text.setReadOnly(True)
# Append log signal
self.log_text.append(message)
```

---

## ✅ Best Practices Checklist
- [ ] Luôn dùng QThread cho tasks mất > 0.1s
- [ ] Xử lý Exception trong thread và báo về UI
- [ ] Disable nút Start khi đang chạy
- [ ] Cấu trúc code rõ ràng (Imports -> Thread -> Window -> Main)
- [ ] Sử dụng Type Hinting cho code dễ đọc
