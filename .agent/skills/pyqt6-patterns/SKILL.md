---
name: pyqt6-patterns
description: Best practices and patterns for building robust PyQt6 desktop applications
---

# PyQt6 Patterns Skill

Guide for building Desktop applications with PyQt6, focusing on architecture, threading, and user experience.

## 🏗️ Architecture Pattern

Use a model that separates UI and Logic:

1.  **MainWindow**: Manages UI, Layout, Signals.
2.  **Worker Thread (QThread)**: Handles long-running tasks (IO, Network, Heavy computation).
3.  **Core Logic**: Pure Python functions, independent of GUI.

### Example Structure `main.py`
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

**Inviolable Rule:** NEVER run heavy tasks on the Main Thread.

### Why?
- Blocks Main Thread -> UI freezes (Not Responding).
- On macOS: Causes "Beachball of death".

### Standard Pattern
Use `QThread`:
1. Create a class inheriting from `QThread`.
2. Define Signals (`pyqtSignal`) to communicate back to Main Thread.
3. Override `run()` method.
4. Initialize and keep reference to thread (`self.thread`) in MainWindow.
5. Connect signals and call `start()`.

---

## 🎨 UI & Layouts

### Layout Hierarchy
Always use Layouts for responsive UI:
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
Use Fusion style for a clean cross-platform look:
```python
app = QApplication(sys.argv)
app.setStyle("Fusion")
```

---

## ⚠️ Error Handling

### Pattern: Try-Except-Signal
In Worker Thread, always use try-except and emit error signal:

```python
def run(self):
    try:
        # Dangerous code
        do_work()
    except Exception as e:
        self.error.emit(str(e)) # Send error to UI
    ```

In UI, listen for signal and show MessageBox:
```python
def on_error(self, message):
    self.btn_start.setEnabled(True) # Re-enable UI
    QMessageBox.critical(self, "Error", message)
```

---

## 📝 Widget Common Patterns

### File Browsing
```python
path = QFileDialog.getExistingDirectory(self, "Select Folder")
if path:
    self.input_dir = path
    self.label.setText(path)
```

### Progress Bar
- **Unknown duration**: `progressBar.setRange(0, 0)`
- **Known duration**: `emit(percent)` from thread -> `progressBar.setValue(percent)`

### Logs Display
Use `QTextEdit` readonly to display realtime logs:
```python
self.log_text = QTextEdit()
self.log_text.setReadOnly(True)
# Append log signal
self.log_text.append(message)
```

---

## ✅ Best Practices Checklist
- [ ] Always using QThread for tasks taking > 0.1s
- [ ] Handling Exceptions in thread and reporting to UI
- [ ] Disabling Start button while running
- [ ] Clear code structure (Imports -> Thread -> Window -> Main)
- [ ] Using Type Hinting for readable code
