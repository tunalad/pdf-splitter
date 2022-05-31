#!/usr/bin/env python
import sys
from ntpath import basename
from os import system, mkdir, path, chdir

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QFileDialog

import pdf_handler


def temp_dir():
    try:
        mkdir(path.join(".", "tempfiles"))
    except OSError as e:
        print(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/pdf-splitter.ui", self)

        self.pdf_path = ""

        self.show()

        # groupboxes
        self.gb_select.toggled.connect(lambda: self.gb_range.setChecked(False))
        self.gb_range.toggled.connect(lambda: self.gb_select.setChecked(False))

        self.btn_open.clicked.connect(lambda: self.add_pages_item())
        self.btn_split_sel.clicked.connect(self.get_selected_items)

        # populating pages listwidget
        self.lw_pages.clear()


    def add_pages_item(self):
        self.pdf_path, _ = QFileDialog.getOpenFileName(self, "Select a PDF file", "", "PDF Files (*.pdf);;All Files (*)")

        if self.pdf_path != "":
            pdf = pdf_handler.file(self.pdf_path)
            pdf_pages = pdf.get_pages()
            pdf.to_images()

            self.lw_pages.clear()
            for page in range(len(pdf_pages)):
                pic = QtGui.QIcon(f"tempfiles/{page}.jpeg")
                item = QListWidgetItem(pic, str(page))
                self.lw_pages.addItem(item)


    def get_selected_items(self):
        items = self.lw_pages.selectedIndexes()
        pdf = pdf_handler.file(self.pdf_path)
        pdf_pages = pdf.get_pages()

        pages_array = []

        if self.cb_merge.isChecked():
            for i in sorted(items):
                pages_array.append(i.row())
            pdf.extract_array(pdf_pages, pages_array)
        else:
            out_dir = basename(self.pdf_path).replace(".pdf", "") + " - [pdf-splitter]"

            try:
                mkdir(path.join(".", out_dir ))
            except OSError as e:
                print(e)

            chdir(out_dir)

            for i in sorted(items):
                pages_array.append(i.row())

            for p in pages_array:
                pdf.extract_page(pdf_pages, p)

            chdir("..")





if __name__ == "__main__":
    # pdf = pdf_handler.file(pdf_path)
    # pages = pdf.get_pages()

    # pdf.to_images()
    # pdf.extract_page(pages, 0)
    # pdf.extract_array(pages, [0, 2, 4])

    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()
