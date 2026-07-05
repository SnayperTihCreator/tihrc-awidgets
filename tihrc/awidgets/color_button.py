from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QPushButton, QColorDialog


class ColorButton(QPushButton):
    color_changed = Signal(QColor)

    def __init__(self, color=Qt.GlobalColor.white, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        self.pressed.connect(self._handle_pressed)

    def _handle_pressed(self):
        color = QColorDialog.getColor(self.color, self, "Выберите цвет")
        if color.isValid():
            self.set_color(color)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            color_rect = self.rect().adjusted(10, 10, -10, -10)
            painter.fillRect(color_rect, self.color)
            painter.drawRect(color_rect)
            painter.setPen(Qt.GlobalColor.black if self.color.lightness() > 128 else Qt.GlobalColor.white)
            painter.drawText(self.rect(), "Выбрать цвет", Qt.AlignmentFlag.AlignCenter)

    def set_color(self, color):
        self.color = color
        self.color_changed.emit(color)
        self.update()

    def get_color(self):
        return self.color
