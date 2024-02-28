#!/usr/bin/env python
import sys
from pprint import pprint
from tempfile import gettempdir
from ntpath import basename
from os import mkdir, path, chdir
import threading

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QMessageBox,
    QProgressBar,
)

import pdf_handler


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/pdf-splitter.ui", self)
        self.setMinimumSize(854, 480)

        self.pdf_path = ""

        self.show()

        # groupboxes
        self.gb_select.toggled.connect(self.toggle_checkboxes)
        self.gb_range.toggled.connect(self.toggle_checkboxes)

        # buttons
        # self.btn_open.clicked.connect(lambda: self.add_pages())
        self.btn_open.clicked.connect(
            lambda: threading.Thread(target=self.add_pages).start()
        )
        self.btn_split_sel.clicked.connect(self.split_selection)
        self.btn_split_range.clicked.connect(self.split_range)

        # list widget drag & drop
        self.lw_pages.setAcceptDrops(True)
        self.lw_pages.dragEnterEvent = self.dragEnterEvent
        self.lw_pages.dragLeaveEvent = self.dragLeaveEvent
        self.lw_pages.dragMoveEvent = self.dragMoveEvent
        self.lw_pages.dropEvent = self.dropEvent

        # clear list
        self.lw_pages.clear()

    # DRAG & DROP
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
            self.lw_pages.setStyleSheet("background-color: rgb(131, 131, 131);")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.lw_pages.setStyleSheet("background-color: rgb(171, 171, 171);")

    def dragMoveEvent(self, event):
        event.accept() if event.mimeData().hasText() else event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            self.add_pages(event.mimeData().urls()[0].toLocalFile())

    # CHECKBOXES
    def toggle_checkboxes(self, state):
        if self.gb_select.isChecked() and self.gb_range.isChecked():
            if self.sender() == self.gb_select:
                self.gb_range.setChecked(False)
            else:
                self.gb_select.setChecked(False)

    # PDF HANDLING
    def add_pages(self, drop_path=None):
        try:
            if not drop_path:
                self.pdf_path, _ = QFileDialog.getOpenFileName(
                    self, "Select a PDF file", "", "PDF Files (*.pdf);;All Files (*)"
                )
            else:
                self.pdf_path = drop_path

            if self.pdf_path != "":
                pdf = pdf_handler.file(self.pdf_path)
                pdf_pages = pdf.get_pages()

                # progress bar
                self.progressbar = QProgressBar()
                self.progressbar.setFormat("Loading the PDF file %p%")
                self.progressbar.setRange(0, len(pdf_pages) * 2)
                self.statusbar.addWidget(self.progressbar)

                # signal
                pdf.progress_signal.connect(
                    lambda: self.progressbar.setValue(self.progressbar.value() + 1)
                )

                pdf.to_images()

                self.lw_pages.clear()
                for page in range(len(pdf_pages)):
                    pic = QtGui.QIcon(f"{gettempdir()}/pdf-splitter-py/{page}.jpeg")
                    item = QListWidgetItem(pic, str(page))
                    self.lw_pages.addItem(item)

                    self.progressbar.setValue(self.progressbar.value() + 1)

                self.statusbar.removeWidget(self.progressbar)
                QMessageBox.information(self, "pdf-splitter", "PDF loaded")
        except Exception as e:
            if str(e).startswith("PDF starts with"):
                QMessageBox.warning(self, "pdf-splitter", "PDF file must be selected")
            else:
                QMessageBox.critical(self, "pdf-splitter", str(e))

    def split_selection(self):
        out_path = QFileDialog.getExistingDirectory(self, "Select output destination")
        if out_path == "" or self.pdf_path == "":
            return None

        items = self.lw_pages.selectedIndexes()
        pdf = pdf_handler.file(self.pdf_path)
        pdf_pages = pdf.get_pages()

        pages_array = []

        if self.cb_merge.isChecked():  # export into single file
            for i in sorted(items):
                pages_array.append(i.row())
            pdf.extract_array(pdf_pages, pages_array, out_path)
        else:  # export pages into a folder
            out_dir = (
                out_path
                or path.dirname(self.pdf_path)
                + "/"
                + basename(self.pdf_path).replace(".pdf", "")
                + " - [pdf-splitter]"
            )
            print(out_dir)

            try:
                mkdir(path.join(".", out_dir))
            except OSError as e:
                print(e)

            chdir(out_dir)

            for i in sorted(items):
                pages_array.append(i.row())

            for p in pages_array:
                pdf.extract_page(pdf_pages, p)

            chdir("..")

        QMessageBox.about(
            self,
            "pdf-splitter",
            f"PDF has been split. <br>The output file is located at: {out_path}",
        )

    def split_range(self):
        try:
            out_path = QFileDialog.getExistingDirectory(
                self, "Select output destination"
            )
            pdf = pdf_handler.file(self.pdf_path)
            pdf_pages = pdf.get_pages()
            pages_array = []

            e_from = int(self.le_from.text())
            e_to = int(self.le_to.text())

            if not (e_from > e_to):
                self.l_from.setStyleSheet("color: black")
                self.l_to.setStyleSheet("color: black")

                if e_from == e_to:
                    pdf.extract_page(e_from)
                else:
                    for i in range(e_from, e_to + 1):
                        pages_array.append(i)
                    pdf.extract_array(pdf_pages, pages_array, out_path)

            else:
                self.l_from.setStyleSheet("color: red")
                self.l_to.setStyleSheet("color: red")

            QMessageBox.about(
                self,
                "pdf-splitter",
                f"PDF has been split. <br>The output file is located at: {out_path}",
            )

        except:
            self.l_from.setStyleSheet("color: red")
            self.l_to.setStyleSheet("color: red")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()
