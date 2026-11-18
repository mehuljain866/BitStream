"""BitStream desktop application — PySide6 interface."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QProgressBar,
    QScrollArea, QSizePolicy, QSpinBox, QStackedWidget, QVBoxLayout, QWidget,
)

try:
    import index as backend
except Exception as exc:  # Surface the real import error in the UI.
    backend = None
    BACKEND_IMPORT_ERROR = exc
else:
    BACKEND_IMPORT_ERROR = None


COLORS = {
    "window": "#101419", "surface": "#171E25", "surface_2": "#202A33",
    "line": "#303C47", "text": "#F1F5F7", "muted": "#9AAAB5",
    "cyan": "#65E8D5", "blue": "#438DFF", "yellow": "#F2C66D",
    "red": "#F07878", "green": "#70D6A7",
}

STYLESHEET = f"""
QWidget {{ background: {COLORS['window']}; color: {COLORS['text']}; font-family: 'Segoe UI', 'Inter', sans-serif; font-size: 13px; }}
QMainWindow {{ background: {COLORS['window']}; }}
QFrame#topbar {{ background: #141A20; border-bottom: 1px solid {COLORS['line']}; }}
QFrame#panel {{ background: {COLORS['surface']}; border: 1px solid {COLORS['line']}; border-radius: 12px; }}
QFrame#subpanel {{ background: {COLORS['surface_2']}; border: 1px solid {COLORS['line']}; border-radius: 9px; }}
QLabel#brand {{ font-size: 19px; font-weight: 700; letter-spacing: 0.4px; }}
QLabel#eyebrow {{ color: {COLORS['cyan']}; font-size: 10px; font-weight: 800; letter-spacing: 1.6px; }}
QLabel#hero {{ font-size: 29px; font-weight: 750; letter-spacing: -0.7px; }}
QLabel#muted {{ color: {COLORS['muted']}; }}
QLabel#section {{ font-size: 15px; font-weight: 700; }}
QLabel#metric {{ color: {COLORS['cyan']}; font-size: 12px; font-weight: 700; }}
QPushButton {{ background: {COLORS['surface_2']}; color: {COLORS['text']}; border: 1px solid #43515D; border-radius: 7px; padding: 9px 14px; font-weight: 650; }}
QPushButton:hover {{ background: #293744; border-color: {COLORS['cyan']}; }}
QPushButton:pressed {{ background: #111820; }}
QPushButton:disabled {{ color: #66737C; background: #1A2026; border-color: #303940; }}
QPushButton#primary {{ background: {COLORS['cyan']}; color: #071311; border: 1px solid {COLORS['cyan']}; font-size: 14px; font-weight: 800; padding: 12px 18px; }}
QPushButton#primary:hover {{ background: #8AF4E5; }}
QPushButton#secondary {{ background: transparent; border: 1px solid {COLORS['line']}; }}
QPushButton#tab {{ background: transparent; border: none; border-bottom: 2px solid transparent; border-radius: 0; color: {COLORS['muted']}; padding: 13px 15px; }}
QPushButton#tab:checked {{ color: {COLORS['text']}; border-bottom: 2px solid {COLORS['cyan']}; }}
QListWidget {{ background: #11171D; border: 1px solid {COLORS['line']}; border-radius: 8px; padding: 5px; outline: none; }}
QListWidget::item {{ padding: 10px 9px; border-bottom: 1px solid #26313A; border-radius: 4px; }}
QListWidget::item:selected {{ background: #233B40; color: {COLORS['text']}; }}
QComboBox, QSpinBox {{ background: #11171D; border: 1px solid #43515D; border-radius: 6px; padding: 8px 10px; min-height: 20px; }}
QComboBox:hover, QSpinBox:hover {{ border-color: {COLORS['cyan']}; }}
QComboBox QAbstractItemView {{ background: #1B242C; selection-background-color: #28514F; }}
QCheckBox {{ spacing: 9px; }}
QCheckBox::indicator {{ width: 17px; height: 17px; border: 1px solid #64737E; border-radius: 4px; background: #11171D; }}
QCheckBox::indicator:checked {{ background: {COLORS['cyan']}; border-color: {COLORS['cyan']}; }}
QProgressBar {{ background: #0D1217; border: 1px solid #3B4A55; border-radius: 5px; height: 12px; text-align: center; color: transparent; }}
QProgressBar::chunk {{ background: {COLORS['cyan']}; border-radius: 4px; }}
QScrollArea {{ border: none; }}
QToolTip {{ background: #202A33; color: {COLORS['text']}; border: 1px solid #52616D; padding: 5px; }}
"""


def clear_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink(missing_ok=True)


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} TB"


class JobWorker(QThread):
    progress = Signal(float, str)
    succeeded = Signal(str)
    failed = Signal(str)

    def __init__(self, operation, parent=None):
        super().__init__(parent)
        self.operation = operation

    def run(self):
        try:
            result = self.operation(lambda value, message: self.progress.emit(float(value), str(message)))
            self.succeeded.emit(str(result))
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")


class SettingsDialog(QDialog):
    def __init__(self, current: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BitStream settings")
        self.setMinimumWidth(390)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(14)
        title = QLabel("ENCODING SETTINGS")
        title.setObjectName("eyebrow")
        layout.addWidget(title)
        layout.addWidget(QLabel("Frame resolution"))
        self.resolution = QComboBox()
        self.resolution.addItems(["256x256", "512x512", "1024x1024", "1920x1080"])
        self.resolution.setCurrentText(current.get("resolution", "256x256"))
        layout.addWidget(self.resolution)
        layout.addWidget(QLabel("Frame rate"))
        self.fps = QComboBox()
        self.fps.addItems(["15", "24", "30", "60"])
        self.fps.setCurrentText(str(current.get("fps", 24)))
        layout.addWidget(self.fps)
        self.steg = QCheckBox("Enable LSB steganography mode")
        self.steg.setChecked(bool(current.get("steganography", False)))
        layout.addWidget(self.steg)
        self.auto_sort = QCheckBox("Sort recovered files by type")
        self.auto_sort.setChecked(bool(current.get("auto_sort", False)))
        layout.addWidget(self.auto_sort)
        note = QLabel("Steganography requires a cover video with enough frame capacity.")
        note.setObjectName("muted")
        note.setWordWrap(True)
        layout.addWidget(note)
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def values(self) -> dict:
        return {
            "resolution": self.resolution.currentText(),
            "fps": int(self.fps.currentText()),
            "steganography": self.steg.isChecked(),
            "auto_sort": self.auto_sort.isChecked(),
        }


class BitStreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BitStream")
        self.setMinimumSize(900, 650)
        self.resize(1120, 760)
        self.setAcceptDrops(True)
        self.worker = None
        self.busy = False
        self.selected_video: Path | None = None
        self.cover_path: Path | None = None
        self.settings = backend.load_settings() if backend else {}
        if backend:
            existing_covers = [p for p in backend.COVER_DIR.iterdir() if p.is_file()]
            self.cover_path = existing_covers[0] if existing_covers else None
        self._build_ui()
        self.refresh_files()
        self.refresh_mode()
        if BACKEND_IMPORT_ERROR:
            self.set_status(f"Backend unavailable: {BACKEND_IMPORT_ERROR}", "error")

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(28, 22, 28, 22)
        outer.setSpacing(18)

        top = QFrame()
        top.setObjectName("topbar")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 13)
        mark = QLabel("B")
        mark.setAlignment(Qt.AlignCenter)
        mark.setFixedSize(34, 34)
        mark.setStyleSheet(f"background:{COLORS['cyan']}; color:#081311; border-radius:8px; font-size:20px; font-weight:900;")
        brand = QLabel("BitStream")
        brand.setObjectName("brand")
        tagline = QLabel("LOSSLESS DATA / VIDEO")
        tagline.setObjectName("eyebrow")
        top_layout.addWidget(mark)
        top_layout.addWidget(brand)
        top_layout.addSpacing(12)
        top_layout.addWidget(tagline)
        top_layout.addStretch(1)
        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("secondary")
        self.settings_button.clicked.connect(self.open_settings)
        top_layout.addWidget(self.settings_button)
        outer.addWidget(top)

        intro = QHBoxLayout()
        intro_left = QVBoxLayout()
        eyebrow = QLabel("EXPERIMENTAL STORAGE SYSTEM  /  CONTAINER V1")
        eyebrow.setObjectName("eyebrow")
        hero = QLabel("Files <span style='color:{COLORS['cyan']}'>→</span> Video")
        hero.setObjectName("hero")
        hero.setTextFormat(Qt.RichText)
        sub = QLabel("Encode archives into lossless video frames. Recover them with integrity checks.")
        sub.setObjectName("muted")
        intro_left.addWidget(eyebrow)
        intro_left.addWidget(hero)
        intro_left.addWidget(sub)
        intro.addLayout(intro_left)
        intro.addStretch(1)
        self.status_pill = QLabel("●  READY")
        self.status_pill.setStyleSheet(f"color:{COLORS['green']}; background:#172820; border:1px solid #315442; border-radius:12px; padding:7px 12px; font-size:11px; font-weight:800;")
        self.status_pill.setAlignment(Qt.AlignCenter)
        intro.addWidget(self.status_pill, 0, Qt.AlignTop)
        outer.addLayout(intro)

        tabs = QHBoxLayout()
        self.encode_tab = QPushButton("01   ENCODE")
        self.decode_tab = QPushButton("02   DECODE")
        for button in (self.encode_tab, self.decode_tab):
            button.setObjectName("tab")
            button.setCheckable(True)
            tabs.addWidget(button)
        tabs.addStretch(1)
        self.encode_tab.clicked.connect(lambda: self.switch_page(0))
        self.decode_tab.clicked.connect(lambda: self.switch_page(1))
        outer.addLayout(tabs)

        self.pages = QStackedWidget()
        self.pages.addWidget(self._build_encode_page())
        self.pages.addWidget(self._build_decode_page())
        outer.addWidget(self.pages, 1)

        progress_panel = QFrame()
        progress_panel.setObjectName("panel")
        progress_layout = QVBoxLayout(progress_panel)
        progress_layout.setContentsMargins(18, 14, 18, 14)
        progress_layout.setSpacing(8)
        progress_head = QHBoxLayout()
        self.progress_label = QLabel("PROCESSING STATUS")
        self.progress_label.setObjectName("eyebrow")
        self.progress_text = QLabel("Ready when you are")
        self.progress_text.setObjectName("muted")
        self.progress_percent = QLabel("0%")
        self.progress_percent.setObjectName("metric")
        progress_head.addWidget(self.progress_label)
        progress_head.addStretch(1)
        progress_head.addWidget(self.progress_text)
        progress_head.addSpacing(16)
        progress_head.addWidget(self.progress_percent)
        progress_layout.addLayout(progress_head)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar)
        outer.addWidget(progress_panel)

        footer = QHBoxLayout()
        self.footer_left = QLabel("FFV1  ·  RGB CHANNEL STORAGE  ·  SHA-256")
        self.footer_left.setObjectName("muted")
        self.footer_left.setStyleSheet("font-size:10px; letter-spacing:1px;")
        footer.addWidget(self.footer_left)
        footer.addStretch(1)
        self.output_button = QPushButton("Open output folder ↗")
        self.output_button.setObjectName("secondary")
        self.output_button.clicked.connect(self.open_output)
        footer.addWidget(self.output_button)
        outer.addLayout(footer)
        self.switch_page(0)

    def _build_encode_page(self):
        page = QWidget()
        layout = QGridLayout(page)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(14)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)

        source = QFrame()
        source.setObjectName("panel")
        sl = QVBoxLayout(source)
        sl.setContentsMargins(18, 18, 18, 18)
        sl.setSpacing(12)
        sh = QHBoxLayout()
        st = QLabel("01 / SOURCE FILES")
        st.setObjectName("eyebrow")
        self.file_count = QLabel("0 ITEMS")
        self.file_count.setObjectName("metric")
        sh.addWidget(st)
        sh.addStretch(1)
        sh.addWidget(self.file_count)
        sl.addLayout(sh)
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.setMinimumHeight(210)
        self.file_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sl.addWidget(self.file_list, 1)
        file_actions = QHBoxLayout()
        add_files = QPushButton("＋  Add files")
        add_folder = QPushButton("＋  Add folder")
        remove = QPushButton("Remove selected")
        remove.setObjectName("secondary")
        add_files.clicked.connect(self.add_files)
        add_folder.clicked.connect(self.add_folder)
        remove.clicked.connect(self.remove_selected)
        file_actions.addWidget(add_files)
        file_actions.addWidget(add_folder)
        file_actions.addWidget(remove)
        sl.addLayout(file_actions)
        drop_hint = QLabel("You can also drag files and folders into this window.")
        drop_hint.setObjectName("muted")
        sl.addWidget(drop_hint)
        layout.addWidget(source, 0, 0, 2, 1)

        destination = QFrame()
        destination.setObjectName("panel")
        dl = QVBoxLayout(destination)
        dl.setContentsMargins(18, 18, 18, 18)
        dl.setSpacing(12)
        dt = QLabel("02 / VIDEO OUTPUT")
        dt.setObjectName("eyebrow")
        dl.addWidget(dt)
        motif = QFrame()
        motif.setObjectName("subpanel")
        motif_layout = QVBoxLayout(motif)
        motif_layout.setContentsMargins(15, 16, 15, 16)
        motif_layout.setSpacing(8)
        flow = QHBoxLayout()
        file_mark = QLabel("FILES")
        file_mark.setStyleSheet(f"font-size:14px; font-weight:900; color:{COLORS['cyan']}; letter-spacing:1px;")
        arrow = QLabel("⟶")
        arrow.setStyleSheet(f"font-size:23px; color:{COLORS['blue']}; font-weight:700;")
        video_mark = QLabel("VIDEO")
        video_mark.setStyleSheet(f"font-size:14px; font-weight:900; color:{COLORS['cyan']}; letter-spacing:1px;")
        flow.addWidget(file_mark)
        flow.addStretch(1)
        flow.addWidget(arrow)
        flow.addStretch(1)
        flow.addWidget(video_mark)
        motif_layout.addLayout(flow)
        caption = QLabel("ARCHIVE  →  FFV1 CONTAINER")
        caption.setObjectName("muted")
        caption.setStyleSheet("font-size:10px; letter-spacing:1px;")
        motif_layout.addWidget(caption)
        dl.addWidget(motif)

        mode_row = QHBoxLayout()
        mode_label = QLabel("Encoding mode")
        mode_label.setObjectName("muted")
        self.mode_value = QLabel("NORMAL")
        self.mode_value.setObjectName("metric")
        mode_row.addWidget(mode_label)
        mode_row.addStretch(1)
        mode_row.addWidget(self.mode_value)
        dl.addLayout(mode_row)
        self.cover_button = QPushButton("Choose cover video")
        self.cover_button.clicked.connect(self.choose_cover)
        dl.addWidget(self.cover_button)
        self.cover_label = QLabel("No cover video selected")
        self.cover_label.setObjectName("muted")
        self.cover_label.setWordWrap(True)
        dl.addWidget(self.cover_label)
        self.encode_button = QPushButton("ENCODE VIDEO  →")
        self.encode_button.setObjectName("primary")
        self.encode_button.setMinimumHeight(48)
        self.encode_button.clicked.connect(self.run_encode)
        dl.addStretch(1)
        dl.addWidget(self.encode_button)
        layout.addWidget(destination, 0, 1, 2, 1)
        return page

    def _build_decode_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 4, 0, 4)
        outer.setSpacing(14)
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)
        eyebrow = QLabel("01 / SOURCE VIDEO")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Recover your archive")
        title.setStyleSheet("font-size:23px; font-weight:750;")
        desc = QLabel("Select a BitStream video. The embedded header identifies normal or steganographic mode automatically.")
        desc.setObjectName("muted")
        desc.setWordWrap(True)
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(desc)
        self.decode_file_label = QLabel("No video selected")
        self.decode_file_label.setObjectName("muted")
        self.decode_file_label.setStyleSheet(f"background:#11171D; border:1px dashed #52616D; border-radius:8px; padding:24px;")
        self.decode_file_label.setAlignment(Qt.AlignCenter)
        self.decode_file_label.setMinimumHeight(100)
        layout.addWidget(self.decode_file_label)
        actions = QHBoxLayout()
        choose = QPushButton("Choose BitStream video")
        choose.clicked.connect(self.choose_decode_video)
        actions.addWidget(choose)
        actions.addStretch(1)
        self.decode_button = QPushButton("VERIFY & EXTRACT  →")
        self.decode_button.setObjectName("primary")
        self.decode_button.setMinimumHeight(46)
        self.decode_button.clicked.connect(self.run_decode)
        actions.addWidget(self.decode_button)
        layout.addLayout(actions)
        outer.addWidget(panel)
        outer.addStretch(1)
        return page

    def switch_page(self, index: int):
        self.pages.setCurrentIndex(index)
        self.encode_tab.setChecked(index == 0)
        self.decode_tab.setChecked(index == 1)

    def refresh_files(self):
        if not backend:
            return
        self.file_list.clear()
        files = [p for p in backend.INPUT_DIR.rglob("*") if p.is_file()]
        for path in files:
            relative = path.relative_to(backend.INPUT_DIR)
            item = QListWidgetItem(f"{relative.as_posix()}     ·     {human_size(path.stat().st_size)}")
            item.setData(Qt.UserRole, str(path))
            self.file_list.addItem(item)
        total = sum(p.stat().st_size for p in files)
        self.file_count.setText(f"{len(files)} ITEMS  ·  {human_size(total)}")

    def add_files(self):
        if not self._require_backend():
            return
        names, _ = QFileDialog.getOpenFileNames(self, "Add files to archive")
        if not names:
            return
        try:
            backend.INPUT_DIR.mkdir(parents=True, exist_ok=True)
            for name in names:
                source = Path(name)
                target = backend.INPUT_DIR / source.name
                if target.exists():
                    target = backend.INPUT_DIR / f"{source.stem}_copy{source.suffix}"
                shutil.copy2(source, target)
            self.refresh_files()
            self.set_status("Files added to archive", "ready")
        except Exception as exc:
            self.show_error("Could not add files", str(exc))

    def add_folder(self):
        if not self._require_backend():
            return
        name = QFileDialog.getExistingDirectory(self, "Add folder to archive")
        if not name:
            return
        source = Path(name)
        target = backend.INPUT_DIR / source.name
        if target.exists():
            target = backend.INPUT_DIR / f"{source.name}_copy"
        try:
            backend.INPUT_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)
            self.refresh_files()
            self.set_status("Folder added to archive", "ready")
        except Exception as exc:
            self.show_error("Could not add folder", str(exc))

    def remove_selected(self):
        if not self._require_backend():
            return
        selected = self.file_list.selectedItems()
        if not selected:
            return
        for item in selected:
            path = Path(item.data(Qt.UserRole))
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink(missing_ok=True)
            except OSError as exc:
                self.show_error("Could not remove item", str(exc))
                return
        self.refresh_files()

    def choose_cover(self):
        if not self._require_backend():
            return
        name, _ = QFileDialog.getOpenFileName(self, "Choose cover video", "", "Video files (*.avi *.mkv *.mp4 *.mov);;All files (*)")
        if not name:
            return
        import cv2
        source = Path(name)
        cap = cv2.VideoCapture(str(source))
        try:
            if not cap.isOpened():
                raise ValueError("OpenCV cannot open this video.")
            ok, frame = cap.read()
            if not ok or frame is None:
                raise ValueError("The selected video contains no readable frames.")
        finally:
            cap.release()
        clear_dir(backend.COVER_DIR)
        backend.COVER_DIR.mkdir(parents=True, exist_ok=True)
        destination = backend.COVER_DIR / source.name
        shutil.copy2(source, destination)
        self.cover_path = destination
        self.cover_label.setText(f"COVER VIDEO  ·  {source.name}")
        self.set_status("Cover video ready", "ready")

    def open_settings(self):
        if not self._require_backend():
            return
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec() == QDialog.Accepted:
            try:
                self.settings = dialog.values()
                backend.save_settings(self.settings)
                self.refresh_mode()
                self.set_status("Settings saved", "ready")
            except Exception as exc:
                self.show_error("Settings could not be saved", str(exc))

    def refresh_mode(self):
        if not backend:
            return
        self.settings = backend.load_settings()
        steg = bool(self.settings.get("steganography"))
        self.mode_value.setText("LSB STEGANOGRAPHY" if steg else "NORMAL / FFV1")
        self.cover_button.setVisible(steg)
        self.cover_label.setVisible(steg)
        self.cover_button.setText("Replace cover video" if self.cover_path else "Choose cover video")
        self.cover_label.setText(f"COVER VIDEO  ·  {self.cover_path.name}" if self.cover_path else "No cover video selected")

    def run_encode(self):
        if not self._require_backend() or self.busy:
            return
        if not any(p.is_file() for p in backend.INPUT_DIR.rglob("*")):
            self.show_error("No source files", "Add at least one file or a folder before encoding.")
            return
        if self.settings.get("steganography") and not any(p.is_file() for p in backend.COVER_DIR.iterdir()):
            self.show_error("Cover video required", "Choose a cover video before starting steganography mode.")
            return
        self.start_job(lambda callback: backend.encode(callback), "ENCODING")

    def choose_decode_video(self):
        name, _ = QFileDialog.getOpenFileName(self, "Select BitStream video", "", "Video files (*.avi *.mkv *.mp4 *.mov);;All files (*)")
        if name:
            self.selected_video = Path(name)
            self.decode_file_label.setText(f"SELECTED VIDEO\n{self.selected_video.name}")

    def run_decode(self):
        if not self._require_backend() or self.busy:
            return
        if not self.selected_video or not self.selected_video.is_file():
            self.show_error("No video selected", "Choose a BitStream video to recover.")
            return
        self.start_job(lambda callback: backend.extract(self.selected_video, callback), "VERIFYING & EXTRACTING")

    def start_job(self, operation, label):
        self.busy = True
        self.encode_button.setEnabled(False)
        self.decode_button.setEnabled(False)
        self.settings_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_percent.setText("0%")
        self.progress_text.setText(label)
        self.set_status(label, "working")
        self.worker = JobWorker(operation, self)
        self.worker.progress.connect(self.on_progress)
        self.worker.succeeded.connect(self.on_success)
        self.worker.failed.connect(self.on_failure)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_progress(self, value: float, message: str):
        percent = max(0, min(100, int(value * 100)))
        self.progress_bar.setValue(percent)
        self.progress_percent.setText(f"{percent}%")
        self.progress_text.setText(message)

    def on_success(self, result: str):
        self.progress_bar.setValue(100)
        self.progress_percent.setText("100%")
        self.progress_text.setText("Integrity checks completed")
        self.set_status("COMPLETE", "success")
        self.refresh_files()
        QMessageBox.information(self, "BitStream · Complete", f"Operation completed successfully.\n\n{result}")

    def on_failure(self, message: str):
        self.set_status("OPERATION FAILED", "error")
        self.progress_text.setText("Operation failed")
        self.show_error("BitStream operation failed", message)

    def on_worker_finished(self):
        self.busy = False
        self.encode_button.setEnabled(True)
        self.decode_button.setEnabled(True)
        self.settings_button.setEnabled(True)
        self.worker = None

    def set_status(self, text: str, state: str = "ready"):
        palette = {"ready": (COLORS["green"], "#172820", "#315442"),
                   "working": (COLORS["yellow"], "#302719", "#65502E"),
                   "success": (COLORS["green"], "#172820", "#315442"),
                   "error": (COLORS["red"], "#301D20", "#63363B")}
        color, bg, border = palette.get(state, palette["ready"])
        self.status_pill.setText(f"●  {text.upper()}")
        self.status_pill.setStyleSheet(f"color:{color}; background:{bg}; border:1px solid {border}; border-radius:12px; padding:7px 12px; font-size:11px; font-weight:800;")

    def show_error(self, title: str, message: str):
        QMessageBox.critical(self, title, message)

    def open_output(self):
        if not self._require_backend():
            return
        backend.OUTPUT_VIDEO.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(backend.OUTPUT_VIDEO.resolve())))

    def _require_backend(self) -> bool:
        if backend:
            return True
        self.show_error("Backend unavailable", str(BACKEND_IMPORT_ERROR))
        return False

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if not self._require_backend():
            return
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls() if url.isLocalFile()]
        try:
            backend.INPUT_DIR.mkdir(parents=True, exist_ok=True)
            for source in paths:
                if source.is_file():
                    target = backend.INPUT_DIR / source.name
                    if target.exists():
                        target = backend.INPUT_DIR / f"{source.stem}_copy{source.suffix}"
                    shutil.copy2(source, target)
                elif source.is_dir():
                    target = backend.INPUT_DIR / source.name
                    if target.exists():
                        target = backend.INPUT_DIR / f"{source.name}_copy"
                    shutil.copytree(source, target)
            self.refresh_files()
            self.set_status("Dropped files added", "ready")
            event.acceptProposedAction()
        except Exception as exc:
            self.show_error("Drop failed", str(exc))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("BitStream")
    app.setOrganizationName("BitStream")
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    window = BitStreamWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
