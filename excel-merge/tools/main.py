"""
Excel Merge Master - Desktop App
A PyQt6 GUI to consolidate multiple Excel files into a single master report.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QLineEdit, QComboBox,
    QProgressBar, QGroupBox, QFormLayout, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import pandas as pd


class MergeThread(QThread):
    """Background thread for merging Excel files."""
    
    progress = pyqtSignal(int, str)
    log = pyqtSignal(str)
    finished = pyqtSignal(int, int, int)
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_file, encoding):
        super().__init__()
        self.input_dir = input_dir
        self.output_file = output_file
        self.encoding = encoding
        
    def run(self):
        try:
            # Find Excel files
            excel_extensions = ('.xlsx', '.xls')
            files = []
            
            for f in os.listdir(self.input_dir):
                if f.lower().endswith(excel_extensions):
                    if f.startswith('~$'):
                        self.log.emit(f"⏭️ Skipping temp file: {f}")
                        continue
                    files.append(os.path.join(self.input_dir, f))
            
            if not files:
                self.error.emit("No Excel files found in the selected folder")
                return
            
            self.log.emit(f"📁 Found {len(files)} Excel files\n")
            
            # Merge files
            all_dfs = []
            processed = 0
            skipped = 0
            
            for i, filepath in enumerate(files, 1):
                filename = os.path.basename(filepath)
                self.progress.emit(int(i / len(files) * 100), f"Processing: {filename}")
                
                try:
                    if filepath.lower().endswith('.xlsx'):
                        df = pd.read_excel(filepath, engine='openpyxl')
                    else:
                        df = pd.read_excel(filepath, engine='xlrd')
                    
                    if df.empty:
                        self.log.emit(f"⚠️ Empty file: {filename}")
                        skipped += 1
                        continue
                    
                    # Add metadata
                    df['Source_File'] = filename
                    df['Row_Index'] = range(1, len(df) + 1)
                    
                    all_dfs.append(df)
                    processed += 1
                    self.log.emit(f"✅ {filename} ({len(df)} rows)")
                    
                except Exception as e:
                    self.log.emit(f"❌ Error reading {filename}: {e}")
                    skipped += 1
            
            if not all_dfs:
                self.error.emit("No valid data to merge!")
                return
            
            # Merge and save
            self.log.emit(f"\n📊 Merging {processed} files...")
            master_df = pd.concat(all_dfs, ignore_index=True)
            
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            master_df.to_excel(self.output_file, index=False, engine='openpyxl')
            
            self.finished.emit(processed, skipped, len(master_df))
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Merge Master")
        self.setMinimumSize(700, 550)
        
        self.input_dir = ""
        self.output_dir = ""
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Input section
        input_group = QGroupBox("📂 Input")
        input_layout = QFormLayout(input_group)
        
        self.input_label = QLabel("No folder selected")
        self.input_label.setWordWrap(True)
        btn_browse = QPushButton("Browse Folder")
        btn_browse.clicked.connect(self.browse_folder)
        input_layout.addRow("Source Folder:", self.input_label)
        input_layout.addRow(btn_browse)
        
        self.file_count_label = QLabel("")
        self.file_count_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        input_layout.addRow("Status:", self.file_count_label)
        
        layout.addWidget(input_group)
        
        # Output section
        output_group = QGroupBox("📤 Output")
        output_layout = QFormLayout(output_group)
        
        self.output_label = QLabel("Same as input folder")
        self.output_label.setWordWrap(True)
        btn_output = QPushButton("Browse Output Folder")
        btn_output.clicked.connect(self.browse_output)
        output_layout.addRow("Output Folder:", self.output_label)
        output_layout.addRow(btn_output)
        
        self.output_name = QLineEdit("Master_Report.xlsx")
        output_layout.addRow("Output Filename:", self.output_name)
        
        layout.addWidget(output_group)
        
        # Settings section
        settings_group = QGroupBox("⚙️ Settings")
        settings_layout = QFormLayout(settings_group)
        
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["Auto", "UTF-8", "Latin-1", "CP1252"])
        settings_layout.addRow("Encoding:", self.encoding_combo)
        
        layout.addWidget(settings_group)
        
        # Progress section
        progress_group = QGroupBox("📊 Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("font-family: Consolas, monospace; font-size: 11px;")
        progress_layout.addWidget(self.log_text)
        
        layout.addWidget(progress_group)
        
        # Merge button
        self.btn_merge = QPushButton("🚀 Merge All Files")
        self.btn_merge.setMinimumHeight(50)
        self.btn_merge.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled { background-color: #cccccc; }
        """)
        self.btn_merge.clicked.connect(self.start_merge)
        layout.addWidget(self.btn_merge)
        
    def browse_folder(self):
        """Browse for input folder."""
        path = QFileDialog.getExistingDirectory(self, "Select Folder with Excel Files")
        if path:
            self.input_dir = path
            self.input_label.setText(path)
            
            # Count Excel files
            count = 0
            for f in os.listdir(path):
                if f.lower().endswith(('.xlsx', '.xls')) and not f.startswith('~$'):
                    count += 1
            
            self.file_count_label.setText(f"Found {count} valid Excel files")
            
    def browse_output(self):
        """Browse for output folder."""
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_dir = path
            self.output_label.setText(path)
            
    def start_merge(self):
        """Start the merge process."""
        if not self.input_dir:
            QMessageBox.warning(self, "No Folder", "Please select input folder first")
            return
        
        # Use output_dir if set, otherwise use input_dir
        output_folder = self.output_dir if self.output_dir else self.input_dir
        output_file = os.path.join(output_folder, self.output_name.text())
        encoding = self.encoding_combo.currentText()
        if encoding == "Auto":
            encoding = "utf-8"
        
        self.btn_merge.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        self.thread = MergeThread(self.input_dir, output_file, encoding)
        self.thread.progress.connect(self.on_progress)
        self.thread.log.connect(self.on_log)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()
        
    def on_progress(self, value, message):
        self.progress_bar.setValue(value)
        
    def on_log(self, message):
        self.log_text.append(message)
        
    def on_finished(self, processed, skipped, total_rows):
        self.btn_merge.setEnabled(True)
        self.progress_bar.setValue(100)
        self.log_text.append(f"\n✅ Complete!")
        self.log_text.append(f"   Processed: {processed} files")
        self.log_text.append(f"   Skipped: {skipped} files")
        self.log_text.append(f"   Total rows: {total_rows}")
        
        QMessageBox.information(self, "Success", 
            f"Merged {processed} files!\n\nTotal rows: {total_rows}\nOutput: {self.output_name.text()}")
        
    def on_error(self, message):
        self.btn_merge.setEnabled(True)
        self.log_text.append(f"\n❌ Error: {message}")
        QMessageBox.critical(self, "Error", message)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
