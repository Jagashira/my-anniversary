import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QComboBox, QLineEdit, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from make_album import generate_pdfs


class Worker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, folder, quality, outname):
        super().__init__()
        self.folder = folder
        self.quality = quality
        self.outname = outname

    def run(self):
        try:
            outdir = generate_pdfs(
                self.folder,
                self.quality,
                output_name=self.outname,
                progress_callback=lambda v: self.progress.emit(v)
            )
            self.finished.emit(outdir)
        except Exception as e:
            self.error.emit(str(e))


class AlbumGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Album PDF Generator")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # Folder input
        self.folder_label = QLabel("画像フォルダ：")
        self.folder_button = QPushButton("フォルダを選択")
        self.folder_button.clicked.connect(self.choose_folder)
        self.folder_path = QLineEdit()

        # quality
        self.quality_label = QLabel("画質プリセット：")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["high", "standard", "light"])

        # output folder name
        self.outname_label = QLabel("出力フォルダ名（任意）：")
        self.outname_input = QLineEdit()

        # progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # generate button
        self.generate_button = QPushButton("PDF生成")
        self.generate_button.clicked.connect(self.start_generate)

        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.folder_path)

        layout.addWidget(self.quality_label)
        layout.addWidget(self.quality_combo)

        layout.addWidget(self.outname_label)
        layout.addWidget(self.outname_input)

        layout.addWidget(self.generate_button)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.folder_path.setText(folder)

    def start_generate(self):
        folder = self.folder_path.text().strip()
        if not os.path.isdir(folder):
            QMessageBox.critical(self, "エラー", "フォルダが存在しません。")
            return

        quality = self.quality_combo.currentText()
        outname = self.outname_input.text().strip()

        self.worker = Worker(folder, quality, outname)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.finish)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def update_progress(self, val):
        self.progress.setValue(val)

    def finish(self, outdir):
        QMessageBox.information(self, "完了", f"PDF生成が完了しました！\n\n出力先: {outdir}")
        self.progress.setValue(100)

    def show_error(self, msg):
        QMessageBox.critical(self, "エラー", msg)


def main():
    app = QApplication(sys.argv)
    gui = AlbumGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
