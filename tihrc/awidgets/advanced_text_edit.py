from PySide6.QtGui import QFont, QTextCharFormat, QAction, QKeySequence
from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QFontComboBox, QTextEdit, QSpinBox

from .color_button import ColorButton


class AdvancedTextEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.toolbar = QToolBar()
        self._layout.addWidget(self.toolbar)

        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self._on_font_select)
        self.toolbar.addWidget(self.font_combo)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 100)
        self.size_spin.setValue(14)
        self.size_spin.valueChanged.connect(self._on_font_size)
        self.toolbar.addWidget(self.size_spin)

        self.toolbar.addSeparator()

        self.act_bold = self._add_action("B", QKeySequence.StandardKey.Bold, self._on_select_bold, bold=True)
        self.act_italic = self._add_action("I", QKeySequence.StandardKey.Italic, self._on_select_italic, italic=True)
        self.act_under = self._add_action("U", QKeySequence.StandardKey.Underline, self._on_select_under,
                                          underline=True)
        self.act_strike = self._add_action("S", None, self._on_select_strike, strike=True)

        self.toolbar.addSeparator()

        self.color_btn = ColorButton()
        self.color_btn.color_changed.connect(self._on_change_color)
        self.toolbar.addWidget(self.color_btn)

        self.text_edit = QTextEdit()
        self.text_edit.currentCharFormatChanged.connect(self._update_format)
        self._layout.addWidget(self.text_edit)

    def _add_action(self, text, shortcut, callback, bold=False, italic=False, underline=False, strike=False):
        action = QAction(text, self)
        action.setCheckable(True)
        if shortcut:
            action.setShortcut(shortcut)
        font = QFont("Arial", 12)
        font.setBold(bold)
        font.setItalic(italic)
        font.setUnderline(underline)
        font.setStrikeOut(strike)
        action.setFont(font)
        action.triggered.connect(callback)
        self.toolbar.addAction(action)
        return action

    def setFon(self, image_path):
        self.text_edit.setStyleSheet(f"""
            QTextEdit {{
                border-image: url({image_path}) 0 0 0 0 stretch stretch;
                padding: 1px;
                font-size: {self.size_spin.value()}pt;
            }}
        """)

    def toHtml(self):
        return self.text_edit.toHtml()

    def setHtml(self, html):
        self.text_edit.setHtml(html)

    def _on_change_color(self, color):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _on_font_select(self, font: QFont):
        fmt = QTextCharFormat()
        fmt.setFontFamilies([font.family()])
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _on_font_size(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _on_select_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self.act_bold.isChecked() else QFont.Weight.Normal)
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _on_select_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.act_italic.isChecked())
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _on_select_under(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.act_under.isChecked())
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _on_select_strike(self):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(self.act_strike.isChecked())
        self._merge_format_selection(fmt)
        self.text_edit.setFocus()

    def _merge_format_selection(self, format_):
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(format_)
        self.text_edit.mergeCurrentCharFormat(format_)

    def _update_format(self):
        self._set_blocking_signals(True)

        current_fmt = self.text_edit.currentCharFormat()
        self.act_bold.setChecked(current_fmt.fontWeight() == QFont.Weight.Bold)
        self.act_italic.setChecked(current_fmt.fontItalic())
        self.act_under.setChecked(current_fmt.fontUnderline())
        self.act_strike.setChecked(current_fmt.fontStrikeOut())
        self.color_btn.set_color(current_fmt.foreground().color())

        font = current_fmt.font()
        if current_fmt.fontPointSize() > 0:
            self.size_spin.setValue(int(current_fmt.fontPointSize()))
        self.font_combo.setCurrentFont(font)
        self._set_blocking_signals(False)

    def _set_blocking_signals(self, state):
        for w in [self.font_combo, self.size_spin, self.color_btn]:
            w.blockSignals(state)
        for a in [self.act_bold, self.act_italic, self.act_under, self.act_strike]:
            a.blockSignals(state)
