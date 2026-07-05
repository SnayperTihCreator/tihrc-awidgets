import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QSplitter, QGroupBox,
)
from PySide6.QtGui import QFont

from tihrc.awidgets import ColorButton, ValueSlider, AdvancedTextEdit
from tihrc.awidgets.guide_panel import GuidePanel


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("tihrc-awidgets demo")
        self.setMinimumSize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(8, 8, 8, 8)

        color_group = QGroupBox("ColorButton")
        color_layout = QVBoxLayout(color_group)

        self.color_btn = ColorButton()
        self.color_btn.color_changed.connect(lambda c: self.color_label.setText(c.name()))
        color_layout.addWidget(self.color_btn)

        self.color_label = QLabel("#ffffff")
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_layout.addWidget(self.color_label)

        left_layout.addWidget(color_group)

        slider_group = QGroupBox("ValueSlider")
        slider_layout = QVBoxLayout(slider_group)

        self.slider = ValueSlider()
        self.slider.setRange(0, 100)
        self.slider.setValue(42)
        self.slider.valueChanged.connect(lambda v: self.slider_label.setText(str(v)))
        slider_layout.addWidget(self.slider)

        self.slider_label = QLabel("42")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_layout.addWidget(self.slider_label)

        left_layout.addWidget(slider_group)

        editor_group = QGroupBox("AdvancedTextEdit")
        editor_layout = QVBoxLayout(editor_group)

        self.editor = AdvancedTextEdit()
        self.editor.text_edit.setPlaceholderText("Введите текст...")
        editor_layout.addWidget(self.editor)

        left_layout.addWidget(editor_group)

        splitter.addWidget(left)

        self.guide = GuidePanel(url="https://dnd5e.ru")
        splitter.addWidget(self.guide)

        splitter.setSizes([400, 500])
        layout.addWidget(splitter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())
