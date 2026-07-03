from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPalette, QFontMetrics
from PySide6.QtWidgets import QSlider, QApplication, QStyleOptionSlider, QStyle


class ValueSlider(QSlider):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        
        self._value_font = QApplication.font()
        self._value_font.setPointSize(self._value_font.pointSize() - 1)
        
        self._label_font = QApplication.font()
        self._label_font.setPointSize(8)
        
        if orientation == Qt.Orientation.Horizontal:
            self.setMinimumHeight(50)
            self.setStyleSheet("ValueSlider { padding-top: 25px; padding-bottom: 20px; }")
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            pallete = self.palette()
            text_color = pallete.color(QPalette.ColorRole.ButtonText)
            muted_text_color = pallete.color(QPalette.ColorRole.PlaceholderText)
            
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            handle_rect = self.style().subControlRect(
                QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderHandle, self
            )
            
            current_value = f"{self.value()}"
            fm = QFontMetrics(self._value_font)
            text_width = fm.horizontalAdvance(current_value)
            padding_x = 8
            rect = QRect(handle_rect.center().x() - (text_width // 2) - padding_x,
                         12,
                         text_width + (padding_x * 2),
                         20)
            
            if rect.left() < 0:
                rect.moveLeft(0)
            elif rect.right() > self.width():
                rect.moveRight(self.width())
            
            painter.setFont(self._value_font)
            painter.setPen(text_color)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, current_value)
            
            painter.setFont(self._label_font)
            painter.setPen(muted_text_color)
            
            min_str = str(self.minimum())
            max_str = str(self.maximum())
            
            fm_small = QFontMetrics(self._label_font)
            
            min_w = fm_small.horizontalAdvance(min_str)
            min_rect = QRect(0, self.height()-45, min_w, 18)
            
            max_w = fm_small.horizontalAdvance(max_str)
            max_rect = QRect(self.width() - max_w, self.height()-45, max_w, 18)
            
            painter.drawText(min_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, min_str)
            painter.drawText(max_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, max_str)