"""QR Code Download Screen — display QR code for digital delivery.

Customer scans the QR code to download their photos via a gallery link.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .base_screen import BaseScreen
from app_core.config import Config
import qrcode
import io
import os

config = Config.instance()


class QRCodeDownloadScreen(BaseScreen):
    """QR code download screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._gallery_url = None

    def setup_ui(self):
        self.setMinimumSize(1920, 1080)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar
        top_bar = QFrame(self)
        top_bar.setFixedHeight(100)
        top_bar.setStyleSheet("background-color: #0F172A; border-radius: 0;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 20, 30, 20)
        top_layout.setSpacing(16)

        back_btn = QPushButton("←")
        back_btn.setFixedSize(44, 44)
        back_btn.setStyleSheet(
            "QPushButton { color: #94A3B8; font-size: 24px; }"
            "QPushButton:hover { color: #F8FAFC; background-color: #334155; }"
        )
        top_layout.addWidget(back_btn)
        top_layout.addStretch(1)

        session_label = QLabel("Sesi: —")
        session_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'JetBrains Mono', monospace;"
        )
        top_layout.addWidget(session_label)

        layout.addWidget(top_bar)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(20)

        # Step indicator
        steps = ["1", "2", "3", "4"]
        steps_text = ["Scan QR", "Buka link", "Download", "Selesai"]
        step_row = QHBoxLayout()
        step_row.setSpacing(0)
        for i, (num, text) in enumerate(zip(steps, steps_text)):
            step_num = QLabel(num)
            step_num.setStyleSheet(
                "font-size: 24px; font-weight: 900; color: #3B82F6; "
                "font-family: 'JetBrains Mono', monospace;"
            )
            step_row.addWidget(step_num)

            if i < len(steps) - 1:
                arrow = QLabel("→")
                arrow.setStyleSheet(
                    "font-size: 24px; color: #3B82F6; font-weight: 900; "
                    "font-family: 'JetBrains Mono', monospace;"
                )
                step_row.addWidget(arrow)

            step_text = QLabel(text)
            step_text.setStyleSheet(
                "font-size: 16px; color: #64748B; font-family: 'Segoe UI', sans-serif;"
                " margin-left: 12px;"
            )
            step_row.addWidget(step_text)

        card_layout.addLayout(step_row)

        # QR code display area
        qr_area = QLabel("QR CODE")
        qr_area.setStyleSheet(
            "font-size: 20px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
            " margin-top: 16px; text-align: center;"
        )
        card_layout.addWidget(qr_area)

        # QR code image
        qr_img = QLabel()
        qr_img.setAlignment(Qt.AlignCenter)
        qr_img.setStyleSheet(
            "background-color: #0F172A; border-radius: 12px; "
            "border: 3px solid #334155; padding: 20px;"
        )

        # Generate QR code (placeholder)
        qr = qrcode.QRCode(
            version=1, box_size=10, border=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )
        qr.add_data("https://xinoobie.example/gallery/S-12345678")
        qr_img_pix = qr.make_image(fill_color="#3B82F6", back_color="white")
        buf = io.BytesIO()
        qr_img_pix.save(buf, format="PNG")
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue(), "PNG")
        qr_img.setPixmap(pixmap)

        qr_img.setFixedSize(300, 300)
        card_layout.addWidget(qr_img)

        # Download link
        link_label = QLabel("https://xinoobie.example/gallery/S-12345678")
        link_label.setStyleSheet(
            "font-size: 16px; color: #3B82F6; font-family: 'JetBrains Mono', monospace;"
            " word-break: break-all; text-align: center;"
        )
        card_layout.addWidget(link_label)

        # Instructions
        instructions = QLabel(
            "Petunjuk:\n"
            "1. Buka kamera pada ponsel Anda\n"
            "2. Scan QR code di atas\n"
            "3. Klik 'Download' untuk mengunduh foto\n"
            "4. Pilih kualitas yang diinginkan"
        )
        instructions.setStyleSheet(
            "font-size: 16px; color: #94A3B8; line-height: 1.6; "
            "font-family: 'Segoe UI', sans-serif;"
            " margin-top: 8px;"
        )
        card_layout.addWidget(instructions)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        # Back
        back_btn = QPushButton("← Kembali")
        back_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 18px; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        back_btn.clicked.connect(self._on_back)
        btn_row.addWidget(back_btn)

        # Download
        download_btn = QPushButton("Unduh QR Code")
        download_btn.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 700; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
        )
        download_btn.clicked.connect(self._on_download)
        btn_row.addWidget(download_btn)

        card_layout.addLayout(btn_row)

        layout.addWidget(card)

    def _on_back(self):
        """Go back to printing screen."""
        from ..main_window import MainApplicationWindow
        main_win = None
        w = self.parent()
        while w:
            from ..main_window import MainApplicationWindow
            if isinstance(w, MainApplicationWindow):
                main_win = w
                break
            w = w.parent()

        if main_win:
            main_win.show_screen("printing")

    def _on_download(self):
        """Handle QR code download."""
        from PySide6.QtWidgets import QFileDialog

        # Save QR image to file
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan QR Code", str(config.data_dir / "qrcode"),
            "PNG Files (*.png)"
        )
        if save_path:
            try:
                import qrcode
                qr = qrcode.QRCode(
                    version=1, box_size=10, border=2,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                )
                qr.add_data("https://xinoobie.example/gallery/S-12345678")
                qr_img_pix = qr.make_image()
                qr_img_pix.save(save_path, "PNG")
                self.logger.info("QR code saved to %s", save_path)
                QMessageBox.information(
                    self, "Selesai",
                    "QR code berhasil disimpan!\n"
                    "Beri tahu customer untuk scan menggunakan kamera ponsel.",
                )
            except Exception as exc:
                self.logger.error("Failed to save QR code: %s", exc)
                QMessageBox.critical(
                    self, "Error", f"Gagal menyimpan QR code: {exc}"
                )
