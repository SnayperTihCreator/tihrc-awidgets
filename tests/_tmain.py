import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSlider
from tihrc.awidgets import ColorButton, ValueSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.box = QHBoxLayout(widget)
        
        self.color_button = ColorButton()
        self.box.addWidget(self.color_button)
        
        self.value_slider = ValueSlider()
        self.box.addWidget(self.value_slider)
        
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
