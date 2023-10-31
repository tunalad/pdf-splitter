from tempfile import TemporaryDirectory, gettempdir
from os import path, makedirs
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5.QtCore import QObject, pyqtSignal
import fitz


class file(QObject):
    progress_signal = pyqtSignal()

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.pdf_in = open(pdf_path, "rb")
        self.pdf_reader = PdfFileReader(self.pdf_in)

    def get_pages(self):
        pdf_pages = []
        for page in range(self.pdf_reader.numPages):
            pdf_pages.append(self.pdf_reader.getPage(page))
        return pdf_pages

    def to_images(self, resolution=300):
        pdf_document = fitz.open(self.pdf_path)

        # create temp dir
        if not path.exists(f"{gettempdir()}/pdf-splitter-py"):
            makedirs(f"{gettempdir()}/pdf-splitter-py")

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            image = page.get_pixmap(
                matrix=fitz.Matrix(resolution / 72, resolution / 72)
            )
            image.save(f"{gettempdir()}/pdf-splitter-py/{page_num}.jpeg")
            self.progress_signal.emit()

    def extract_page(self, all_pages, page, out_path=None):
        file_name = path.basename(self.pdf_path).replace(".pdf", "")
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(all_pages[page])
        if out_path:
            pdf_out = open(out_path + f"/{file_name}-page-{page}-out.pdf", "wb")
        else:
            pdf_out = open(f"{file_name}-page-{page}-out.pdf", "wb")
        pdf_writer.write(pdf_out)
        pdf_out.close()

    def extract_array(self, all_pages, new_pages, out_path=None):
        file_name = path.basename(self.pdf_path).replace(".pdf", "")
        file_dir = path.dirname(self.pdf_path)
        pdf_writer = PdfFileWriter()
        for i in new_pages:
            pdf_writer.addPage(all_pages[i])
        if out_path:
            pdf_out = open(
                out_path + f"/{file_name}-{len(new_pages)}-pages-out.pdf", "wb"
            )
        else:
            pdf_out = open(
                file_dir + f"/{file_name}-{len(new_pages)}-pages-out.pdf", "wb"
            )
        pdf_writer.write(pdf_out)
        pdf_out.close()
