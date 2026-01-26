"""
Bulk Invitation Generator - Desktop App
A visual tool to design invitation layouts and batch-generate personalized image files.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QFileDialog, QSpinBox,
    QComboBox, QColorDialog, QProgressBar, QGroupBox, QFormLayout,
    QScrollArea, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter, QFont, QFontDatabase
from PIL import Image, ImageDraw, ImageFont
import pandas as pd


class DraggableLabel(QLabel):
    """A label that can be dragged to set text position."""
    
    positionChanged = pyqtSignal(int, int)
    
    def __init__(self, text="Sample Name", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 180);
            border: 2px dashed #333;
            padding: 8px 16px;
            font-size: 18px;
            font-weight: bold;
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragging = False
        self.offset = QPoint()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            # Constrain within parent bounds
            parent = self.parent()
            if parent:
                max_x = parent.width() - self.width()
                max_y = parent.height() - self.height()
                new_pos.setX(max(0, min(new_pos.x(), max_x)))
                new_pos.setY(max(0, min(new_pos.y(), max_y)))
            self.move(new_pos)
            self.positionChanged.emit(new_pos.x(), new_pos.y())
            
    def mouseReleaseEvent(self, event):
        self.dragging = False


class ImageCanvas(QWidget):
    """Canvas widget to display template image with draggable text."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.pixmap = None
        self.original_size = QSize(0, 0)
        self.scale_factor = 1.0
        
        # Draggable text label
        self.text_label = DraggableLabel("Placeholder Name", self)
        self.text_label.move(100, 100)
        self.text_label.adjustSize()
        
    def load_image(self, path):
        """Load and display an image."""
        self.pixmap = QPixmap(path)
        if not self.pixmap.isNull():
            self.original_size = self.pixmap.size()
            self.update_display()
            return True
        return False
        
    def update_display(self):
        """Update the canvas size based on image."""
        if self.pixmap and not self.pixmap.isNull():
            # Scale to fit within max size while maintaining aspect ratio
            max_width = 800
            max_height = 600
            
            scaled = self.pixmap.scaled(
                max_width, max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.scale_factor = scaled.width() / self.original_size.width()
            self.setFixedSize(scaled.size())
            self.update()
            
    def paintEvent(self, event):
        """Draw the image."""
        if self.pixmap and not self.pixmap.isNull():
            painter = QPainter(self)
            scaled = self.pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)
            
    def get_real_coordinates(self):
        """Get text position in original image coordinates."""
        if self.scale_factor > 0:
            label_pos = self.text_label.pos()
            label_center_x = label_pos.x() + self.text_label.width() // 2
            real_x = int(label_center_x / self.scale_factor)
            real_y = int(label_pos.y() / self.scale_factor)
            return real_x, real_y
        return 0, 0
        
    def update_text_style(self, font_family, font_size, color):
        """Update the text label appearance."""
        self.text_label.setStyleSheet(f"""
            background-color: rgba(255, 255, 255, 180);
            border: 2px dashed #333;
            padding: 8px 16px;
            font-family: {font_family};
            font-size: {min(font_size // 2, 24)}px;
            font-weight: bold;
            color: {color};
        """)
        self.text_label.adjustSize()


class GeneratorThread(QThread):
    """Background thread for generating invitations."""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(int)
    error = pyqtSignal(str)
    
    def __init__(self, template_path, guest_file, output_dir, font_path, font_size, font_color, x_pos, y_pos):
        super().__init__()
        self.template_path = template_path
        self.guest_file = guest_file
        self.output_dir = output_dir
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        
    def run(self):
        try:
            # Load guest list
            if self.guest_file.endswith('.csv'):
                df = pd.read_csv(self.guest_file)
            else:
                df = pd.read_excel(self.guest_file)
                
            # Find name column
            name_col = 'Name'
            if name_col not in df.columns:
                name_col = df.columns[0]
                
            # Load template
            template = Image.open(self.template_path)
            img_width = template.size[0]
            
            # Load font
            try:
                font = ImageFont.truetype(self.font_path, self.font_size)
            except:
                font = ImageFont.load_default()
                
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Generate invitations
            total = len(df)
            count = 0
            
            for index, row in df.iterrows():
                name = str(row[name_col]).strip()
                if not name or name.lower() == 'nan':
                    continue
                    
                # Create image copy
                img = template.copy()
                draw = ImageDraw.Draw(img)
                
                # Calculate text position (center horizontally if x_pos is "center")
                try:
                    bbox = draw.textbbox((0, 0), name, font=font)
                    text_width = bbox[2] - bbox[0]
                except:
                    text_width = len(name) * self.font_size // 2
                    
                if self.x_pos == "center":
                    x = (img_width - text_width) // 2
                else:
                    x = self.x_pos - text_width // 2
                    
                # Draw text
                draw.text((x, self.y_pos), name, font=font, fill=self.font_color)
                
                # Save
                safe_name = "".join(c for c in name if c.isalnum() or c in ' .-_').strip()
                filename = f"invitation-{safe_name}.png"
                img.save(os.path.join(self.output_dir, filename))
                
                count += 1
                self.progress.emit(int((count / total) * 100), f"Generated: {name}")
                
            self.finished.emit(count)
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bulk Invitation Generator")
        self.setMinimumSize(1000, 700)
        
        # State
        self.template_path = ""
        self.guest_file = ""
        self.output_dir = ""
        self.font_path = ""
        self.font_color = (255, 255, 255)  # White
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Tab 1: Design
        design_tab = self.create_design_tab()
        tabs.addTab(design_tab, "📐 Design")
        
        # Tab 2: Generate
        generate_tab = self.create_generate_tab()
        tabs.addTab(generate_tab, "⚡ Generate")
        
    def create_design_tab(self):
        """Create the design tab."""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left: Canvas
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setMinimumWidth(650)
        
        self.canvas = ImageCanvas()
        self.canvas.text_label.positionChanged.connect(self.on_position_changed)
        canvas_scroll.setWidget(self.canvas)
        layout.addWidget(canvas_scroll, stretch=2)
        
        # Right: Properties panel
        props_panel = QWidget()
        props_layout = QVBoxLayout(props_panel)
        props_panel.setMaximumWidth(300)
        
        # Template section
        template_group = QGroupBox("Template Image")
        template_layout = QVBoxLayout(template_group)
        
        self.template_label = QLabel("No template loaded")
        self.template_label.setWordWrap(True)
        template_layout.addWidget(self.template_label)
        
        btn_load_template = QPushButton("📂 Load Template")
        btn_load_template.clicked.connect(self.load_template)
        template_layout.addWidget(btn_load_template)
        
        props_layout.addWidget(template_group)
        
        # Position section
        pos_group = QGroupBox("Text Position")
        pos_layout = QFormLayout(pos_group)
        
        self.x_label = QLabel("0")
        self.y_label = QLabel("0")
        pos_layout.addRow("X (center):", self.x_label)
        pos_layout.addRow("Y:", self.y_label)
        
        hint = QLabel("💡 Drag the text box on the canvas to set position")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #666; font-style: italic;")
        pos_layout.addRow(hint)
        
        props_layout.addWidget(pos_group)
        
        # Font section
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Segoe UI", "Tahoma", "Custom..."])
        self.font_combo.currentTextChanged.connect(self.on_font_changed)
        font_layout.addRow("Family:", self.font_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(12, 200)
        self.font_size_spin.setValue(60)
        self.font_size_spin.valueChanged.connect(self.update_preview)
        font_layout.addRow("Size:", self.font_size_spin)
        
        self.color_btn = QPushButton("Choose Color")
        self.color_btn.setStyleSheet("background-color: white; color: black;")
        self.color_btn.clicked.connect(self.choose_color)
        font_layout.addRow("Color:", self.color_btn)
        
        btn_load_font = QPushButton("📂 Load Custom Font")
        btn_load_font.clicked.connect(self.load_custom_font)
        font_layout.addRow(btn_load_font)
        
        self.font_path_label = QLabel("Using system font")
        self.font_path_label.setWordWrap(True)
        self.font_path_label.setStyleSheet("color: #666; font-size: 11px;")
        font_layout.addRow(self.font_path_label)
        
        props_layout.addWidget(font_group)
        
        props_layout.addStretch()
        layout.addWidget(props_panel)
        
        return tab
        
    def create_generate_tab(self):
        """Create the generate tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Guest file section
        guest_group = QGroupBox("Guest List")
        guest_layout = QVBoxLayout(guest_group)
        
        self.guest_label = QLabel("No file loaded")
        self.guest_label.setWordWrap(True)
        guest_layout.addWidget(self.guest_label)
        
        btn_load_guests = QPushButton("📂 Load Guest List (Excel/CSV)")
        btn_load_guests.clicked.connect(self.load_guests)
        guest_layout.addWidget(btn_load_guests)
        
        layout.addWidget(guest_group)
        
        # Output section
        output_group = QGroupBox("Output Directory")
        output_layout = QVBoxLayout(output_group)
        
        self.output_label = QLabel("No directory selected")
        self.output_label.setWordWrap(True)
        output_layout.addWidget(self.output_label)
        
        btn_select_output = QPushButton("📂 Select Output Folder")
        btn_select_output.clicked.connect(self.select_output)
        output_layout.addWidget(btn_select_output)
        
        layout.addWidget(output_group)
        
        # Summary section
        summary_group = QGroupBox("Summary")
        summary_layout = QFormLayout(summary_group)
        
        self.summary_template = QLabel("-")
        self.summary_template.setWordWrap(True)
        summary_layout.addRow("Template:", self.summary_template)
        
        self.summary_font = QLabel("-")
        summary_layout.addRow("Font:", self.summary_font)
        
        self.summary_position = QLabel("-")
        summary_layout.addRow("Position:", self.summary_position)
        
        self.summary_guests = QLabel("-")
        summary_layout.addRow("Guests:", self.summary_guests)
        
        layout.addWidget(summary_group)
        
        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666;")
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Generate button
        self.btn_generate = QPushButton("🚀 Generate Invitations")
        self.btn_generate.setMinimumHeight(50)
        self.btn_generate.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.btn_generate.clicked.connect(self.start_generation)
        layout.addWidget(self.btn_generate)
        
        layout.addStretch()
        
        return tab
        
    def load_template(self):
        """Load template image."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Template Image",
            "", "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.template_path = path
            if self.canvas.load_image(path):
                self.template_label.setText(os.path.basename(path))
                self.summary_template.setText(os.path.basename(path))
            else:
                QMessageBox.warning(self, "Error", "Failed to load image")
                
    def load_guests(self):
        """Load guest list file."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Guest List",
            "", "Excel/CSV (*.xlsx *.xls *.csv)"
        )
        if path:
            self.guest_file = path
            try:
                if path.endswith('.csv'):
                    df = pd.read_csv(path)
                else:
                    df = pd.read_excel(path)
                count = len(df)
                self.guest_label.setText(f"{os.path.basename(path)} ({count} guests)")
                self.summary_guests.setText(str(count))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to read file: {e}")
                
    def select_output(self):
        """Select output directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_dir = path
            self.output_label.setText(path)
            
    def load_custom_font(self):
        """Load custom font file."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Font File",
            "", "Font Files (*.ttf *.otf)"
        )
        if path:
            self.font_path = path
            self.font_path_label.setText(os.path.basename(path))
            self.font_combo.setCurrentText("Custom...")
            self.update_preview()
            
    def choose_color(self):
        """Open color dialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = (color.red(), color.green(), color.blue())
            self.color_btn.setStyleSheet(
                f"background-color: {color.name()}; color: {'black' if color.lightness() > 128 else 'white'};"
            )
            self.update_preview()
            
    def on_font_changed(self, text):
        """Handle font family change."""
        if text != "Custom...":
            # Map to system font paths
            font_map = {
                "Arial": "C:/Windows/Fonts/arial.ttf",
                "Times New Roman": "C:/Windows/Fonts/times.ttf",
                "Segoe UI": "C:/Windows/Fonts/segoeui.ttf",
                "Tahoma": "C:/Windows/Fonts/tahoma.ttf",
            }
            self.font_path = font_map.get(text, "")
            self.font_path_label.setText(f"Using: {text}")
        self.update_preview()
        
    def on_position_changed(self, x, y):
        """Handle position change from canvas."""
        real_x, real_y = self.canvas.get_real_coordinates()
        self.x_label.setText(str(real_x))
        self.y_label.setText(str(real_y))
        self.summary_position.setText(f"X={real_x}, Y={real_y}")
        
    def update_preview(self):
        """Update text preview on canvas."""
        font_family = self.font_combo.currentText()
        if font_family == "Custom...":
            font_family = "Arial"
        font_size = self.font_size_spin.value()
        color = f"rgb({self.font_color[0]}, {self.font_color[1]}, {self.font_color[2]})"
        self.canvas.update_text_style(font_family, font_size, color)
        self.summary_font.setText(f"{font_family}, {font_size}px")
        
    def start_generation(self):
        """Start the generation process."""
        # Validate inputs
        if not self.template_path:
            QMessageBox.warning(self, "Missing Input", "Please load a template image first.")
            return
        if not self.guest_file:
            QMessageBox.warning(self, "Missing Input", "Please load a guest list file first.")
            return
        if not self.output_dir:
            QMessageBox.warning(self, "Missing Input", "Please select an output directory first.")
            return
            
        # Get position
        real_x, real_y = self.canvas.get_real_coordinates()
        
        # Get font path
        font_path = self.font_path
        if not font_path or not os.path.exists(font_path):
            font_path = "C:/Windows/Fonts/arial.ttf"
            
        # Disable button
        self.btn_generate.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Start thread
        self.thread = GeneratorThread(
            self.template_path,
            self.guest_file,
            self.output_dir,
            font_path,
            self.font_size_spin.value(),
            self.font_color,
            "center",  # Always center X
            real_y
        )
        self.thread.progress.connect(self.on_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()
        
    def on_progress(self, value, message):
        """Handle progress update."""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        
    def on_finished(self, count):
        """Handle generation complete."""
        self.btn_generate.setEnabled(True)
        self.progress_bar.setValue(100)
        self.status_label.setText(f"✅ Complete! Generated {count} invitations.")
        QMessageBox.information(self, "Success", f"Generated {count} invitation cards!\n\nOutput: {self.output_dir}")
        
    def on_error(self, message):
        """Handle error."""
        self.btn_generate.setEnabled(True)
        self.status_label.setText(f"❌ Error: {message}")
        QMessageBox.critical(self, "Error", message)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set dark palette for modern look
    palette = app.palette()
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
