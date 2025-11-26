import sys
import os

from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QProgressBar, QMessageBox,
    QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QButtonGroup,QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtCore import QTimer

from generate_pdfs import generate_pdfs

class DropLineEdit(QLineEdit):
    def __init__(self, parent=None, mode="folder"):
        super().__init__(parent)
        self.mode = mode   # "folder" または "text"
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            path = event.mimeData().urls()[0].toLocalFile()
            if self.mode == "folder" and os.path.isdir(path):
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            path = event.mimeData().urls()[0].toLocalFile()
            if self.mode == "folder" and os.path.isdir(path):
                self.setText(path)




# ==============================
#  PDF 生成スレッド（UIフリーズ防止）
# ==============================
class GenerateThread(QThread):
    progress = pyqtSignal(float)   # ★ int → float に変更
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, folder, quality, outname, filename):
        super().__init__()
        self.folder = folder
        self.quality = quality
        self.outname = outname
        self.filename = filename

    def run(self):
        try:
            outdir = generate_pdfs(
                self.folder,
                self.quality,
                output_name=self.outname if self.outname else None,
                custom_filename=self.filename if self.filename else None,
                progress_callback=lambda p: self.progress.emit(float(p))
            )
            self.finished.emit(outdir)
        except Exception as e:
            self.error.emit(str(e))


class MacSuccessDialog(QDialog):
    def __init__(self, outdir: str, parent=None):
        super().__init__(parent)
        self.outdir = outdir

        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(360, 190)

        self.setStyleSheet("""
            QDialog {
                background: white;
                border-radius: 14px;
            }
            QLabel#Title {
                font-family: "SF Pro Text", "Helvetica Neue", Arial;
                font-size: 17px;
                font-weight: 600;
                color: #1A1A1A;
            }
            QPushButton {
                font-family: "SF Pro Text";
                font-size: 15px;
                padding: 8px 22px;
                border-radius: 10px;
            }
            QPushButton#openBtn {
                background: #E5E5EA;
                color: #111;
            }
            QPushButton#okBtn {
                background-color: #007AFF;
                color: white;
            }
        """)

        layout = QVBoxLayout()
        title = QLabel("PDF の生成が完了しました")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btnRow = QHBoxLayout()
        openBtn = QPushButton("フォルダを開く")
        openBtn.setObjectName("openBtn")
        openBtn.clicked.connect(self.open_folder)
        btnRow.addWidget(openBtn)

        okBtn = QPushButton("OK")
        okBtn.setObjectName("okBtn")
        okBtn.clicked.connect(self.accept)
        btnRow.addWidget(okBtn)

        layout.addLayout(btnRow)
        self.setLayout(layout)

        # ---- 遅延センタリングでズレを完全排除 ----
        QTimer.singleShot(0, self.center_dialog)


    def center_dialog(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        x = screen_rect.center().x() - self.width() // 2
        y = screen_rect.center().y() - self.height() // 2

        self.move(x, y)

    def open_folder(self):
        os.system(f'open "{self.outdir}"')






# ==============================
#  Apple風 GUI 本体
# ==============================
class AppleStyleAlbumGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anniversary Album Maker ✨")
        self.setFixedSize(640, 640)


        # --------- 全体のスタイル（Apple風） ---------
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5f7fb,
                    stop:1 #e9edf5
                );
                font-family: "Helvetica Neue", "Arial";
                font-size: 14px;
            }
            QLabel {
                color: #1a1a1a;
            }
            QLineEdit {
                border: 1px solid #d0d3da;
                border-radius: 10px;
                padding: 8px 10px;
                background: rgba(255, 255, 255, 0.9);
                color: #1a1a1a;
            }
            QLineEdit:focus {
                border: 1px solid #007AFF;
                background: rgba(255,255,255,1.0);
            }
            QPushButton {
                border-radius: 999px;
                padding: 10px;
                font-size: 15px;
                background-color: #007AFF;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #0062d6;
            }
            QPushButton:pressed {
                background-color: #004fa8;
            }
            QProgressBar {
                height: 12px;
                background: rgba(0,0,0,0.05);
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 6px;
            }
        """)

        # --------- メインレイアウト ---------
        root = QVBoxLayout()
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(24)

        # タイトル
        title = QLabel("写真アルバム PDF 生成ツール")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Helvetica Neue", 22, QFont.Weight.Bold))
        root.addWidget(title)

        # --------- ガラスカード ---------
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background: rgba(255, 255, 255, 0.82);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.9);
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setOffset(0, 18)
        shadow.setColor(QColor(0, 0, 0, 45))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(18)

        # ===== 画像フォルダ =====
        lbl_folder = QLabel("画像フォルダ（ドラッグ＆ドロップも可）")
        self.edit_folder = DropLineEdit(mode="folder")
        self.edit_folder.setPlaceholderText("例: /Users/you/Photos/anniversary/")
        self.btn_browse = QPushButton("フォルダを選択")
        self.btn_browse.clicked.connect(self.select_folder)

        card_layout.addWidget(lbl_folder)
        card_layout.addWidget(self.edit_folder)
        card_layout.addWidget(self.btn_browse)


        # ===== 品質（Apple風セグメント） =====
        lbl_quality = QLabel("品質（Quality）")
        card_layout.addWidget(lbl_quality)

        self.quality_group = QButtonGroup(self)
        self.quality_buttons = {}  # key -> QPushButton

        seg_layout = QHBoxLayout()
        seg_layout.setSpacing(0)

        options = [("high", "High"), ("standard", "Standard"), ("light", "Light")]
        for idx, (key, label) in enumerate(options):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            # セグメント風スタイル
            radius_left = "10px" if idx == 0 else "0px"
            radius_right = "10px" if idx == len(options) - 1 else "0px"
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255,255,255,0.8);
                    border: 1px solid #d0d3da;
                    padding: 6px 16px;
                    font-size: 14px;
                    border-top-left-radius: {radius_left};
                    border-bottom-left-radius: {radius_left};
                    border-top-right-radius: {radius_right};
                    border-bottom-right-radius: {radius_right};
                    color: #1a1a1a;
                }}
                QPushButton:hover {{
                    background: rgba(230,230,230,0.9);
                }}
                QPushButton:checked {{
                    background: #007AFF;
                    color: white;
                    border: 1px solid #0077EE;
                }}
                QPushButton:checked:hover {{
                    background: #0062d6;
                }}
            """)

            if key == "high":
                btn.setChecked(True)

            self.quality_group.addButton(btn)
            self.quality_buttons[key] = btn
            seg_layout.addWidget(btn)

        card_layout.addLayout(seg_layout)

        # ===== 出力フォルダ名 =====
        lbl_outname = QLabel("出力フォルダ名（任意）")
        self.edit_outname = DropLineEdit(mode="folder")
        self.edit_outname.setPlaceholderText("空の場合は画像フォルダ名が使われます")
        card_layout.addWidget(lbl_outname)
        card_layout.addWidget(self.edit_outname)

        # ===== 出力ファイル名 =====
        lbl_filename = QLabel("出力ファイル名（任意・拡張子不要）")
        self.edit_filename = QLineEdit()
        self.edit_filename.setPlaceholderText("例: my_anniversary_album")
        card_layout.addWidget(lbl_filename)
        card_layout.addWidget(self.edit_filename)

        # ===== 進捗バー =====
        self.progress = QProgressBar()
        self.progress.setValue(0)
        card_layout.addWidget(self.progress)

        # ===== 生成ボタン =====
        self.btn_generate = QPushButton("PDF を生成する")
        self.btn_generate.clicked.connect(self.start_generate)
        card_layout.addWidget(self.btn_generate)

        card.setLayout(card_layout)
        root.addWidget(card)

        self.setLayout(root)

    def set_ui_enabled(self, enabled: bool):
    # 生成ボタン
        self.btn_generate.setEnabled(enabled)

    # フォルダ選択ボタン
        self.btn_browse.setEnabled(enabled)

    # 入力欄
        self.edit_folder.setEnabled(enabled)
        self.edit_outname.setEnabled(enabled)
        self.edit_filename.setEnabled(enabled)

    # 品質セグメント（3つのボタン）
        for btn in self.quality_buttons.values():
            btn.setEnabled(enabled)

    # # ------------------ ドラッグ＆ドロップ ------------------
    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         # 1つ目のURLがフォルダなら受け入れる
    #         urls = event.mimeData().urls()
    #         if urls:
    #             path = urls[0].toLocalFile()
    #             if os.path.isdir(path):
    #                 event.acceptProposedAction()

    # def dropEvent(self, event):
    #     urls = event.mimeData().urls()
    #     if urls:
    #         path = urls[0].toLocalFile()
    #         if os.path.isdir(path):
    #             self.edit_folder.setText(path)

    # ------------------ フォルダ選択 ------------------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "画像フォルダを選択")
        if folder:
            self.edit_folder.setText(folder)

    # ------------------ 生成開始 ------------------
    def start_generate(self):
        folder = self.edit_folder.text().strip()
        if not folder or not os.path.isdir(folder):
            QMessageBox.critical(self, "エラー", "有効な画像フォルダを選択してください。")
            return

        # Quality（セグメントから取得）
        quality = "high"
        for key, btn in self.quality_buttons.items():
            if btn.isChecked():
                quality = key
                break

        outname = self.edit_outname.text().strip()
        filename = self.edit_filename.text().strip()

        self.progress.setValue(0)

        self.set_ui_enabled(False)

        self.worker = GenerateThread(folder, quality, outname, filename)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    # ------------------ コールバック ------------------
    def update_progress(self, v: float):
        self.progress.setValue(int(v * 100))   # ★ 0〜1 → 0〜100


    def on_finished(self, outdir: str):
        dlg = MacSuccessDialog(outdir, None)
        dlg.exec()
        self.progress.setValue(100)
        self.set_ui_enabled(True)

    def on_error(self, msg: str):
        QMessageBox.critical(self, "エラー", f"PDF 生成中にエラーが発生しました。\n\n{msg}")
        self.set_ui_enabled(True)


# ==============================
#  エントリポイント
# ==============================
def main():
    app = QApplication(sys.argv)
    gui = AppleStyleAlbumGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
