"""
E-commerce Watermark Pro - Desktop App
A visual tool to position watermarks and batch process product images.
"""

import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QSlider, QSpinBox,
    QProgressBar, QGroupBox, QFormLayout, QGraphicsScene,
    QGraphicsView, QGraphicsPixmapItem, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF
from PyQt6.QtGui import QPixmap, QPen, QColor, QBrush
from PIL import Image, ImageOps


class DraggablePixmapItem(QGraphicsPixmapItem):
    """A pixmap item that can be dragged."""
    
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
    def itemChange(self, change, value):
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemPositionChange:
            # Constrain within scene bounds if needed
            pass
        return super().itemChange(change, value)


class ProcessorThread(QThread):
    """Background thread for batch processing images."""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(int, int)
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_dir, watermark_path, 
                 canvas_size, opacity, wm_scale, wm_pos):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.watermark_path = watermark_path
        self.canvas_size = canvas_size
        self.opacity = opacity
        self.wm_scale = wm_scale
        self.wm_pos = wm_pos  # (x_ratio, y_ratio) relative to canvas
        
    def run(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Get list of images
            supported = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')
            images = [f for f in os.listdir(self.input_dir) 
                      if f.lower().endswith(supported)]
            
            if not images:
                self.error.emit("No images found in input folder")
                return
                
            # Load watermark
            watermark = None
            if self.watermark_path and os.path.exists(self.watermark_path):
                watermark = Image.open(self.watermark_path).convert('RGBA')
                
            total = len(images)
            processed = 0
            errors = 0
            
            for i, filename in enumerate(images, 1):
                try:
                    input_path = os.path.join(self.input_dir, filename)
                    output_name = os.path.splitext(filename)[0] + '.jpg'
                    output_path = os.path.join(self.output_dir, output_name)
                    
                    # Load and process image
                    img = Image.open(input_path)
                    
                    # Convert mode
                    if img.mode in ('RGBA', 'P'):
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = bg
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Smart resize with padding
                    img = ImageOps.pad(img, (self.canvas_size, self.canvas_size), 
                                       color=(255, 255, 255))
                    
                    # Apply watermark
                    if watermark:
                        wm = watermark.copy()
                        
                        # Scale watermark
                        wm_width = int(self.canvas_size * self.wm_scale / 100)
                        ratio = wm_width / wm.width
                        wm_height = int(wm.height * ratio)
                        wm = wm.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
                        
                        # Apply opacity
                        alpha = wm.split()[3]
                        alpha = alpha.point(lambda p: int(p * self.opacity / 100))
                        wm.putalpha(alpha)
                        
                        # Calculate position
                        x = int(self.wm_pos[0] * self.canvas_size - wm_width / 2)
                        y = int(self.wm_pos[1] * self.canvas_size - wm_height / 2)
                        
                        # Paste watermark
                        img_rgba = img.convert('RGBA')
                        img_rgba.paste(wm, (x, y), wm)
                        img = img_rgba.convert('RGB')
                    
                    # Save
                    img.save(output_path, 'JPEG', quality=90)
                    processed += 1
                    self.progress.emit(int(i / total * 100), f"Processed: {filename}")
                    
                except Exception as e:
                    errors += 1
                    self.progress.emit(int(i / total * 100), f"Error: {filename}")
                    
            self.finished.emit(processed, errors)
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-commerce Watermark Pro")
        self.setMinimumSize(1100, 700)
        
        # State
        self.input_dir = ""
        self.output_dir = ""
        self.watermark_path = ""
        self.base_image_path = ""
        self.input_images = []  # List of images in input folder
        self.current_preview_index = -1
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout with splitter
        main_layout = QHBoxLayout(central)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(350)
        
        # Files section
        files_group = QGroupBox("📂 Files")
        files_layout = QFormLayout(files_group)
        
        # Input folder
        self.input_label = QLabel("Not selected")
        self.input_label.setWordWrap(True)
        btn_input = QPushButton("Select Input Folder")
        btn_input.clicked.connect(self.select_input)
        files_layout.addRow("Input:", self.input_label)
        files_layout.addRow(btn_input)
        
        # Output folder
        self.output_label = QLabel("Not selected")
        self.output_label.setWordWrap(True)
        btn_output = QPushButton("Select Output Folder")
        btn_output.clicked.connect(self.select_output)
        files_layout.addRow("Output:", self.output_label)
        files_layout.addRow(btn_output)
        
        # Watermark
        self.wm_label = QLabel("Not selected")
        self.wm_label.setWordWrap(True)
        btn_wm = QPushButton("Select Watermark PNG")
        btn_wm.clicked.connect(self.select_watermark)
        files_layout.addRow("Watermark:", self.wm_label)
        files_layout.addRow(btn_wm)
        
        # Preview controls
        preview_row = QHBoxLayout()
        btn_base = QPushButton("📷 Load Custom")
        btn_base.clicked.connect(self.load_preview_image)
        self.btn_next_preview = QPushButton("🔀 Next Preview")
        self.btn_next_preview.clicked.connect(self.load_random_preview)
        self.btn_next_preview.setEnabled(False)
        preview_row.addWidget(btn_base)
        preview_row.addWidget(self.btn_next_preview)
        files_layout.addRow("Preview:", preview_row)
        
        left_layout.addWidget(files_group)
        
        # Settings section
        settings_group = QGroupBox("⚙️ Watermark Settings")
        settings_layout = QFormLayout(settings_group)
        
        # Opacity slider
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(70)
        self.opacity_slider.valueChanged.connect(self.update_preview)
        self.opacity_label = QLabel("70%")
        opacity_row = QHBoxLayout()
        opacity_row.addWidget(self.opacity_slider)
        opacity_row.addWidget(self.opacity_label)
        settings_layout.addRow("Opacity:", opacity_row)
        
        # Scale slider
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(5, 50)
        self.scale_slider.setValue(30)
        self.scale_slider.valueChanged.connect(self.update_preview)
        self.scale_label = QLabel("30%")
        scale_row = QHBoxLayout()
        scale_row.addWidget(self.scale_slider)
        scale_row.addWidget(self.scale_label)
        settings_layout.addRow("Scale:", scale_row)
        
        # Canvas size
        self.canvas_spin = QSpinBox()
        self.canvas_spin.setRange(500, 2000)
        self.canvas_spin.setValue(1000)
        self.canvas_spin.setSingleStep(100)
        settings_layout.addRow("Canvas Size:", self.canvas_spin)
        
        left_layout.addWidget(settings_group)
        
        # Progress section
        progress_group = QGroupBox("📊 Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready - Drag watermark to position it")
        self.status_label.setStyleSheet("color: #666;")
        progress_layout.addWidget(self.status_label)
        
        left_layout.addWidget(progress_group)
        
        # Start button
        self.btn_start = QPushButton("🚀 Start Processing")
        self.btn_start.setMinimumHeight(50)
        self.btn_start.setStyleSheet("""
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
        self.btn_start.clicked.connect(self.start_processing)
        left_layout.addWidget(self.btn_start)
        
        left_layout.addStretch()
        
        # Right panel - Canvas
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        canvas_label = QLabel("📐 Preview Canvas (Drag watermark to position)")
        canvas_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_layout.addWidget(canvas_label)
        
        # Graphics scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setMinimumSize(600, 600)
        self.view.setStyleSheet("background-color: #f0f0f0; border: 2px solid #ccc;")
        right_layout.addWidget(self.view)
        
        # Position display
        self.pos_label = QLabel("Position: Center (0.5, 0.5)")
        right_layout.addWidget(self.pos_label)
        
        # Add to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 650])
        
        # Initialize scene
        self.base_item = None
        self.wm_item = None
        self.init_scene()
        
    def init_scene(self):
        """Initialize the graphics scene with placeholder."""
        self.scene.clear()
        
        # Draw canvas placeholder
        canvas_size = 500  # Display size
        rect = self.scene.addRect(0, 0, canvas_size, canvas_size,
                                  QPen(QColor("#ccc")),
                                  QBrush(QColor("#ffffff")))
        
        # Add center text
        text = self.scene.addText("Load a preview image\nor drag watermark here")
        text.setDefaultTextColor(QColor("#999"))
        text.setPos(canvas_size/2 - 80, canvas_size/2 - 20)
        
    def select_input(self):
        """Select input folder."""
        path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if path:
            self.input_dir = path
            # Get list of images
            supported = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')
            self.input_images = [os.path.join(path, f) for f in os.listdir(path) 
                                 if f.lower().endswith(supported)]
            count = len(self.input_images)
            self.input_label.setText(f"{os.path.basename(path)} ({count} images)")
            
            # Enable Next Preview button and load random preview
            if count > 0:
                self.btn_next_preview.setEnabled(True)
                self.load_random_preview()
            else:
                self.btn_next_preview.setEnabled(False)
            
    def select_output(self):
        """Select output folder."""
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_dir = path
            self.output_label.setText(os.path.basename(path))
            
    def select_watermark(self):
        """Select watermark file."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Watermark", "", "PNG Images (*.png)"
        )
        if path:
            self.watermark_path = path
            self.wm_label.setText(os.path.basename(path))
            self.update_preview()
            
    def load_preview_image(self):
        """Load a base image for preview from file dialog."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "", "Images (*.jpg *.jpeg *.png *.webp)"
        )
        if path:
            self.base_image_path = path
            self.update_preview()
            
    def load_random_preview(self):
        """Load a random image from input folder as preview."""
        if not self.input_images:
            return
        
        # Pick a random image (different from current if possible)
        if len(self.input_images) > 1:
            available = [i for i in range(len(self.input_images)) 
                        if i != self.current_preview_index]
            self.current_preview_index = random.choice(available)
        else:
            self.current_preview_index = 0
            
        self.base_image_path = self.input_images[self.current_preview_index]
        self.update_preview()
        
        # Update status
        filename = os.path.basename(self.base_image_path)
        self.status_label.setText(f"Preview: {filename} ({self.current_preview_index + 1}/{len(self.input_images)})")
        
            
    def update_preview(self):
        """Update the preview canvas with smart resize simulation."""
        self.opacity_label.setText(f"{self.opacity_slider.value()}%")
        self.scale_label.setText(f"{self.scale_slider.value()}%")
        
        self.scene.clear()
        canvas_display = 500
        
        # Always draw white canvas background first (simulates the output)
        self.scene.addRect(0, 0, canvas_display, canvas_display,
                          QPen(QColor("#ccc")), QBrush(QColor("#ffffff")))
        
        # Draw base image centered (simulating smart resize with padding)
        if self.base_image_path and os.path.exists(self.base_image_path):
            pixmap = QPixmap(self.base_image_path)
            # Scale to fit within canvas while keeping aspect ratio
            pixmap = pixmap.scaled(canvas_display, canvas_display,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            # Center the image on the canvas
            x_offset = (canvas_display - pixmap.width()) / 2
            y_offset = (canvas_display - pixmap.height()) / 2
            self.base_item = self.scene.addPixmap(pixmap)
            self.base_item.setPos(x_offset, y_offset)
        
        # Draw watermark
        if self.watermark_path and os.path.exists(self.watermark_path):
            wm_pixmap = QPixmap(self.watermark_path)
            # Scale watermark
            scale = self.scale_slider.value() / 100
            wm_size = int(canvas_display * scale)
            wm_pixmap = wm_pixmap.scaledToWidth(wm_size, Qt.TransformationMode.SmoothTransformation)
            
            self.wm_item = DraggablePixmapItem(wm_pixmap)
            self.wm_item.setOpacity(self.opacity_slider.value() / 100)
            # Center position
            x = (canvas_display - wm_pixmap.width()) / 2
            y = (canvas_display - wm_pixmap.height()) / 2
            self.wm_item.setPos(x, y)
            self.scene.addItem(self.wm_item)
            
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
    def get_watermark_position(self):
        """Get watermark position as ratio (0-1)."""
        if self.wm_item:
            canvas_display = 500
            pos = self.wm_item.pos()
            wm_rect = self.wm_item.boundingRect()
            center_x = (pos.x() + wm_rect.width() / 2) / canvas_display
            center_y = (pos.y() + wm_rect.height() / 2) / canvas_display
            return (max(0, min(1, center_x)), max(0, min(1, center_y)))
        return (0.5, 0.5)  # Default center
        
    def start_processing(self):
        """Start batch processing."""
        if not self.input_dir:
            QMessageBox.warning(self, "Missing Input", "Please select input folder")
            return
        if not self.output_dir:
            QMessageBox.warning(self, "Missing Output", "Please select output folder")
            return
            
        self.btn_start.setEnabled(False)
        self.progress_bar.setValue(0)
        
        wm_pos = self.get_watermark_position()
        self.pos_label.setText(f"Position: ({wm_pos[0]:.2f}, {wm_pos[1]:.2f})")
        
        self.thread = ProcessorThread(
            self.input_dir,
            self.output_dir,
            self.watermark_path,
            self.canvas_spin.value(),
            self.opacity_slider.value(),
            self.scale_slider.value(),
            wm_pos
        )
        self.thread.progress.connect(self.on_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()
        
    def on_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        
    def on_finished(self, processed, errors):
        self.btn_start.setEnabled(True)
        self.progress_bar.setValue(100)
        self.status_label.setText(f"✅ Done! Processed: {processed}, Errors: {errors}")
        QMessageBox.information(self, "Complete", 
            f"Processed {processed} images!\nErrors: {errors}\n\nOutput: {self.output_dir}")
        
    def on_error(self, message):
        self.btn_start.setEnabled(True)
        self.status_label.setText(f"❌ Error: {message}")
        QMessageBox.critical(self, "Error", message)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
