from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import (
    QDockWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QWidget,
    QLabel,
)
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView


_shared_profile: QWebEngineProfile | None = None


def _get_profile(name: str = "qtyrant") -> QWebEngineProfile:
    global _shared_profile
    if _shared_profile is None:
        _shared_profile = QWebEngineProfile(name)
        _shared_profile.setPersistentCookiesPolicy(
            QWebEngineProfile.ForcePersistentCookies
        )
        _shared_profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        _shared_profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
    return _shared_profile


class GuidePanel(QDockWidget):
    def __init__(self, url: str = "https://dnd5e.ru", title: str = "Справочник",
                 profile_name: str = "qtyrant", parent=None):
        super().__init__(title, parent)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        nav = QHBoxLayout()
        self._btn_back = QPushButton("\u2190")
        self._btn_back.setFixedWidth(30)
        self._btn_back.clicked.connect(self._go_back)
        nav.addWidget(self._btn_back)

        self._btn_forward = QPushButton("\u2192")
        self._btn_forward.setFixedWidth(30)
        self._btn_forward.clicked.connect(self._go_forward)
        nav.addWidget(self._btn_forward)

        self._url_bar = QLineEdit()
        self._url_bar.returnPressed.connect(self._load_url)
        nav.addWidget(self._url_bar)

        self._status = QLabel()
        self._status.setFixedWidth(120)
        nav.addWidget(self._status)

        layout.addLayout(nav)

        self._profile = _get_profile(profile_name)

        self._page = QWebEnginePage(self._profile, None)
        self._page.urlChanged.connect(self._on_url_changed)
        self._page.loadStarted.connect(self._on_load_started)
        self._page.loadProgress.connect(self._on_load_progress)
        self._page.loadFinished.connect(self._on_load_finished)

        self._view = QWebEngineView()
        self._view.setPage(self._page)
        layout.addWidget(self._view)

        self.setWidget(container)
        self._view.load(QUrl(url))

        self._setup_shortcuts()

    def _setup_shortcuts(self):
        back = QAction("Назад", self)
        back.setShortcut(QKeySequence("Alt+Left"))
        back.triggered.connect(self._go_back)
        self.addAction(back)

        forward = QAction("Вперёд", self)
        forward.setShortcut(QKeySequence("Alt+Right"))
        forward.triggered.connect(self._go_forward)
        self.addAction(forward)

        focus_url = QAction("URL", self)
        focus_url.setShortcut(QKeySequence("Ctrl+L"))
        focus_url.triggered.connect(lambda: self._url_bar.setFocus())
        self.addAction(focus_url)

    def _on_url_changed(self, url: QUrl):
        self._url_bar.setText(url.toString())

    def _on_load_started(self):
        self._status.setText("Загрузка...")

    def _on_load_progress(self, progress: int):
        self._status.setText(f"Загрузка {progress}%")

    def _on_load_finished(self, ok: bool):
        self._status.setText("✓" if ok else "✗ Ошибка")

    def _load_url(self):
        text = self._url_bar.text().strip()
        if text:
            if "://" not in text:
                text = "https://" + text
            self._view.load(QUrl(text))

    def _go_back(self):
        self._view.back()

    def _go_forward(self):
        self._view.forward()
