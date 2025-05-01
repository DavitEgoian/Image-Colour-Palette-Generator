import sys, os
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from color_extractor import ColorExtractor
from palette_saver import PaletteSaver
from PIL import Image

class SuccessPopup(QtWidgets.QDialog):
    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        container = QtWidgets.QFrame()
        container.setStyleSheet(
            """
            QFrame { background: #313131; border-radius: 12px; }
            QLabel { color: #00e676; font-size: 14pt; }
            QPushButton { background: #00e676; color: #212121; border:none; padding:8px 16px; border-radius:6px; }
            QPushButton:hover { background: #66ffa6; }
            """
        )
        vbox = QtWidgets.QVBoxLayout(container)
        vbox.setAlignment(QtCore.Qt.AlignCenter)
        label = QtWidgets.QLabel(message)
        button = QtWidgets.QPushButton('OK')
        button.clicked.connect(self.accept)
        vbox.addWidget(label)
        vbox.addSpacing(10)
        vbox.addWidget(button, alignment=QtCore.Qt.AlignCenter)

        layout.addWidget(container)
        self.resize(300, 120)

class ImagePaletteApp(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Colour Palette Generator')
        self.resize(900, 700)
        self._apply_dark_theme()
        self._init_ui()
        self.colors = []

    def _apply_dark_theme(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(40,40,40))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(30,30,30))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(45,45,45))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(60,60,60))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0,150,136))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        QtWidgets.QApplication.setPalette(palette)

    def _init_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(15)

        toolbar = QtWidgets.QToolBar(); toolbar.setIconSize(QtCore.QSize(28,28)); toolbar.setMovable(False)
        load = QtWidgets.QAction(QtGui.QIcon.fromTheme('folder-open'), 'Upload Image', self); load.triggered.connect(self.upload_image)
        save = QtWidgets.QAction(QtGui.QIcon.fromTheme('document-save'), 'Save Palette', self); save.triggered.connect(self.save_palette); save.setEnabled(False)
        self.save_action = save
        toolbar.addAction(load); toolbar.addSeparator(); toolbar.addAction(save)
        self.addToolBar(toolbar)

        self.image_frame = QtWidgets.QFrame(); self.image_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.image_frame.setStyleSheet('background:#202020; border:2px dashed #555; border-radius:8px;')
        img_layout = QtWidgets.QVBoxLayout(self.image_frame)
        self.image_label = QtWidgets.QLabel('No Image Loaded', alignment=QtCore.Qt.AlignCenter)
        self.image_label.setStyleSheet('color:#888; font-size:18px;')
        img_layout.addWidget(self.image_label)
        self.image_frame.setFixedSize(450,450)
        main_layout.addWidget(self.image_frame, alignment=QtCore.Qt.AlignCenter)

        pal_label = QtWidgets.QLabel('Top 10 Colours:', alignment=QtCore.Qt.AlignLeft)
        pal_label.setStyleSheet('color:#fff; font-size:16px;')
        main_layout.addWidget(pal_label)
        self.palette_widget = QtWidgets.QWidget(); self.palette_layout = QtWidgets.QHBoxLayout(self.palette_widget)
        self.palette_layout.setSpacing(12); self.palette_layout.setContentsMargins(0,0,0,0)
        pal_scroll = QtWidgets.QScrollArea(); pal_scroll.setWidgetResizable(True); pal_scroll.setWidget(self.palette_widget)
        pal_scroll.setFixedHeight(120); pal_scroll.setStyleSheet('background:transparent;')
        main_layout.addWidget(pal_scroll)

        status_layout = QtWidgets.QHBoxLayout()
        self.progress = QtWidgets.QProgressBar(); self.progress.setRange(0,0); self.progress.setVisible(False)
        status_layout.addWidget(self.progress)
        self.status = QtWidgets.QLabel('Ready'); self.status.setStyleSheet('color:#aaa')
        status_layout.addWidget(self.status, alignment=QtCore.Qt.AlignRight)
        main_layout.addLayout(status_layout)

    def upload_image(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if not path: return
        self.status.setText(f'Loaded {os.path.basename(path)}')
        img = Image.open(path)
        self.colors = ColorExtractor(img).top_colors(10)
        pix = QtGui.QPixmap(path).scaled(450,450,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
        self.image_label.setPixmap(pix); self.image_label.setText('')
        self._display_palette(); self.save_action.setEnabled(True)

    def _display_palette(self):
        while self.palette_layout.count():
            w = self.palette_layout.takeAt(0).widget(); w.deleteLater()
        for color in self.colors:
            swatch = QtWidgets.QFrame(); swatch.setFixedSize(80,80)
            swatch.setStyleSheet(f'border-radius:6px; background:{self.rgb_to_hex(color)};')
            effect = QtWidgets.QGraphicsDropShadowEffect(blurRadius=10, xOffset=0, yOffset=2)
            swatch.setGraphicsEffect(effect)
            self.palette_layout.addWidget(swatch)
        self.status.setText('Palette Generated')

    def save_palette(self):
        default = f"palette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Palette', default, 'PNG Files (*.png)')
        if not path: return
        self.progress.setVisible(True); self.status.setText('Saving…')
        QtCore.QTimer.singleShot(150, lambda: self._save(path))

    def _save(self, path):
        PaletteSaver(self.colors).save(path)
        self.progress.setVisible(False); self.status.setText(f'Saved {os.path.basename(path)}')
        popup = SuccessPopup('Palette Saved!')
        popup.exec_()

    @staticmethod
    def rgb_to_hex(color: tuple[int,int,int]) -> str:
        return '#{:02X}{:02X}{:02X}'.format(*color)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImagePaletteApp(); window.show(); sys.exit(app.exec_())